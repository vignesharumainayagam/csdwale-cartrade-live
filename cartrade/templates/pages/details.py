# -*- coding: utf-8 -*-
# Copyright (c) 2018, Tridots Tech Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
# from _future_ import unicode_literals
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
	location = frappe.request.cookies.get('city_location')

	path = frappe.local.request.path

	path = path.replace('csd-', '')

	context.path = path

	path = path.strip('/')

	word = path.split('/')

	item_route= word[2].lower()


	brand_route = word[1]

	category_route = word[0]

	context.category_route = category_route

	context.rightadd = frappe.db.get_value('Widget Placeholder', fieldname=['google_ad_script'], filters={"view": 'Detail View', 'position': 'Right Panel'})
	context.topadd = frappe.db.get_value('Widget Placeholder', fieldname=['google_ad_script'], filters={'view': 'Detail View', 'position': 'Top Panel'})
	context.bottomadd = frappe.db.get_value('Widget Placeholder', fieldname=['google_ad_script'], filters={'view': 'Detail View', 'position': 'Bottom Panel'})
	context.midads = frappe.db.get_value('Widget Placeholder', fieldname=['google_ad_script'], filters={'view': 'Detail View', 'position': 'Middle Panel'})

	category_name = frappe.db.get_value("Category", 
				  	filters={'route': category_route}, fieldname=['category_name'])

	category = frappe.db.get_value("Category", 
				filters={'route': category_route}, fieldname=['name'])

	context.category_name = category_name

	context.brand_route = brand_route

	brand_name = frappe.db.get_value("ItemBrand", 
						 filters={'route': brand_route}, fieldname=['name'])

	context.brand_name = brand_name

	context.item_route = item_route

	context.related_bikes = frappe.db.get_list('Item',
							filters={'brand':brand_name, 'category':category,  "route": ["!=", item_route] }, 
							fields=['item_name', 'featured_image', 'route'])

	context.meta_title = frappe.db.get_value("Item", 
						 filters={'route': item_route}, fieldname=['meta_title'])

	context.meta_description = frappe.db.get_value("Item", 
						 filters={'route': item_route}, fieldname=['meta_description'])

	context.meta_keywords = frappe.db.get_value("Item", 
						 filters={'route': item_route}, fieldname=['meta_keywords'])	

	item = frappe.db.get_all('Item', 
				   fields=['route','item_name', 'brand', 'short_description', 'featured_image', 'name'],
				   filters={'route'.lower(): item_route, 'brand': brand_name, 'category': category},
				   limit_page_length=1)
			

	item = item[0]			
	context.item = item	

	context.item_brand = frappe.db.get_value("ItemBrand", 
						 filters={'name'.lower(): item.brand}, fieldname=['brand_name'])


	item_variants = frappe.db.get_all("Item Variant",
					fields=['route','variant_name', 'brand', 'item', 'name'],
				    filters={'item': item.name},
				    limit_page_length= 100)

	context.lo = frappe.request.cookies.get('city_location')


	for x in item_variants:
		x.current_location = frappe.request.cookies.get('city_location')

		if x.current_location:
			price = frappe.db.get_list('Item Variant Price', 
				fields = ['market_price', 'csd_price','difference'], filters = {'variant': x.name, 'city': location, 'item': item.name})

			if len(price) > 0:
				x.csd_price = price[0].csd_price
				x.market_price = price[0].market_price
				x.difference=price[0].difference
			else:
				x.csd_price = "Na"
				x.market_price = "Na"
				x.difference="Na"
		else:
			price = frappe.db.get_list('Item Variant Price', 
				fields = ['market_price', 'csd_price','difference'], filters = {'variant': x.name, 'city': 'Delhi', 'item': item.name})

			if len(price) > 0:
				x.csd_price = price[0].csd_price
				x.market_price = price[0].market_price
				x.difference=price[0].difference
			else:
				x.csd_price = "Na"
				x.market_price = "Na"
				x.difference="Na"
	context.item_variants = item_variants	
	context.city_route=frappe.request.cookies.get('city_location')

	if not frappe.request.cookies.get('city_location'):
		context.dealers = frappe.db.get_all("Dealers",
									fields=['dealer_name','dealer_address', 'dealer_phone', 'route','name'],
								    filters={'city': "Delhi", "brand": item.brand},
								    limit_page_length= 10)	
	else:	
		context.dealers = frappe.db.get_all("Dealers",
									fields=['dealer_name','dealer_address', 'dealer_phone', 'route','name'],
								    filters={'city': frappe.request.cookies.get('city_location'), "brand": item.brand},
								    limit_page_length= 10)




@frappe.whitelist(allow_guest=True)
def getPriceBasedOnCity(city_name,variant_name,item):
	price = frappe.db.get_list('Item Variant Price', 
				fields = ['market_price', 'csd_price','difference'], 
				filters = {'variant': variant_name, 'city': city_name, 'item': item})
	
 	return price
