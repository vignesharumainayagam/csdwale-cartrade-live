from __future__ import unicode_literals

import frappe
import frappe.utils
from frappe.utils.oauth import get_oauth2_authorize_url, get_oauth_keys, login_via_oauth2, login_via_oauth2_id_token, login_oauth_user as _login_oauth_user, redirect_post_login
import json
from frappe import _
from frappe.auth import LoginManager
from frappe.integrations.doctype.ldap_settings.ldap_settings import get_ldap_settings
from frappe.utils.password import get_decrypted_password
from frappe.utils.html_utils import get_icon_html



def get_context(context):
	path = frappe.local.request.path
	path = path.replace('csd-', '')
	path = path.strip('/')
	path = path.split('/')

	location = frappe.request.cookies.get('city_location')

	category_route = path[0]

	brand_route = path[1]

	context.category_route = category_route

	context.adsright = frappe.db.get_value('Widget Placeholder', fieldname=['google_ad_script'], filters={"view": 'Detail View', 'position': 'Right Panel'})
	context.toptads = frappe.db.get_value('Widget Placeholder', fieldname=['google_ad_script'], filters={'view': 'Detail View', 'position': 'Top Panel'})
	context.bottomads = frappe.db.get_value('Widget Placeholder', fieldname=['google_ad_script'], filters={'view': 'Detail View', 'position': 'Bottom Panel'})
	context.midads = frappe.db.get_value('Widget Placeholder', fieldname=['google_ad_script'], filters={'view': 'Detail View', 'position': 'Middle Panel'})

	Category=frappe.db.get_all('Category', 
								fields=['category_name','route','name'],
							    filters={'route': category_route})

	Brand=frappe.db.get_all('ItemBrand', 
							 fields=['route','name','brand_name','meta_title','meta_description','meta_keywords'],
							 filters={'route':brand_route})

	rowe=frappe.db.get_list('Item Brand Category', filters = {'category': Category[0].name}, fields=['parent'])	
	for x in rowe:
		x.route = frappe.db.get_value('ItemBrand',fieldname=['route'], filters={'name':x.parent})
		x.brand_name = frappe.db.get_value('ItemBrand',fieldname=['brand_name'], filters={'name':x.parent})
		item_count = frappe.db.get_all("Item", fields=['name'], filters={'brand': x.parent, 'category': Category[0].name, 'is_published': 1})
		x.count = len(item_count)	
	context.rowe=rowe

	context.meta_keywords = frappe.db.get_value("ItemBrand", 
						 filters={'route': brand_route}, fieldname=['meta_keywords'])

	context.meta_description = frappe.db.get_value("ItemBrand", 
						 filters={'route': brand_route}, fieldname=['meta_description'])

	context.meta_title = frappe.db.get_value("ItemBrand", 
						 filters={'route': brand_route}, fieldname=['meta_title'])


	ItemList=frappe.db.get_all('Item', 
								fields=['item_name','category','csd_rate','market_rate','route',
										'featured_image','short_description','brand', 'name'],
								filters={'brand':Brand[0].name,'category':Category[0].name, 'is_published':1},
								limit_start=0, limit_page_length=20)

	
	for x in ItemList:
		x.current_location = location
		ItemBrand=frappe.db.get_all('ItemBrand', fields=['route','name','brand_name'],filters={'name':x.brand})
		ItemCategory=frappe.db.get_all('Category', fields=['route','name','category_name'],filters={'name':x.category})
		x.BrandUrl=ItemBrand[0].route
		x.CategoryUrl=ItemCategory[0].route

		if x.current_location:


			market_price = frappe.db.get_list('Item Variant Price', 
				fields = ['market_price'], filters = {'item': x.name, 'city': location})

			if len(market_price) > 0:
				x.base_market_price = min(market_price)
			
			else:
				x.base_market_price = {'market_price': 'Na'}
		
		else:


			market_price = frappe.db.get_list('Item Variant Price', 
				fields = ['market_price'], filters = {'item': x.name, 'city': 'Delhi'})	

			if len(market_price) > 0:
				x.base_market_price = min(market_price)	
			
			else:
				x.base_market_price = {'market_price': 'Na'}


	context.Category=Category
	context.ItemList=ItemList
	context.Brand=Brand
	if Item[0].meta_title:
		context.title=Brand[0].brand_name
	if Item[0].meta_title != None:
		context.title=Brand[0].meta_title


	context.MetaDescription=Brand[0].meta_description
	context.MetaKeywords=Brand[0].meta_keywords
	context.CurrentUrl=frappe.utils.get_url()+path



@frappe.whitelist(allow_guest=True)
def get_more_items(category_route, brand_route,num):

	Category=frappe.db.get_all('Category', 
							  fields=['category_name','route','name'],
							  filters={'route': category_route})

	Brand=frappe.db.get_all('ItemBrand', 
							 fields=['route','name','brand_name','meta_title','meta_description','meta_keywords'],
							 filters={'route':brand_route})

	data = frappe.db.get_all('Item', 
								fields=['item_name','category','csd_rate','market_rate','route',
										'featured_image','short_description','brand', 'name'],
								filters={'brand':Brand[0].name,'category':Category[0].name},
								limit_start = num,limit_page_length=20)

	for x in data:
		x.current_location = frappe.request.cookies.get('city_location')
		ItemBrand=frappe.db.get_all('ItemBrand', fields=['route','name','brand_name'],filters={'name':x.brand})
		ItemCategory=frappe.db.get_all('Category', fields=['route','name','category_name'],filters={'name':x.category})
		x.BrandUrl=ItemBrand[0].route
		x.CategoryUrl=ItemCategory[0].route

		if x.current_location:


			market_price = frappe.db.get_list('Item Variant Price', 
				fields = ['market_price'], filters = {'item': x.name, 'city': frappe.request.cookies.get('city_location')})

			if len(market_price) > 0:
				x.base_market_price = min(market_price)
			
			else:
				x.base_market_price = {'market_price': 'Na'}
		
		else:


			market_price = frappe.db.get_list('Item Variant Price', 
				fields = ['market_price'], filters = {'item': x.name, 'city': 'Delhi'})	

			if len(market_price) > 0:
				x.base_market_price = min(market_price)	
			
			else:
				x.base_market_price = {'market_price': 'Na'}

	return data		


