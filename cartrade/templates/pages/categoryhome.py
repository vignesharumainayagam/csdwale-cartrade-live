# -*- coding: utf-8 -*-
# Copyright (c) 2018, Tridots Tech Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
# from _future_ import unicode_literals
import frappe
import frappe.utils
import json
from frappe import _
import frappe.utils
from frappe.utils import cint, cstr
import frappe.model.meta
import frappe.defaults
import frappe.translate
from frappe.utils.change_log import get_change_log
from six.moves.urllib.parse import unquote
from six import text_type



def get_context(context):
	path = frappe.local.request.path
	
	path = path.replace('csd-', '')

	path = path.replace("/", "")

	
	context.path = path

	location = frappe.request.cookies.get('city_location')

	LatestNews=frappe.db.get_all('News', fields=['title','description','image','category','route'],limit_page_length=6)
	pathcategory = frappe.db.get_list('Category', fields=['name','route'], filters={'route':path.lower()})	
	pathcategoryname = pathcategory[0].name
	context.pathcategoryroute = pathcategory[0].route
	if pathcategoryname.endswith('s'):
		context.pathcategory = pathcategory[0].name[:-1]
	else:
		context.pathcategory = 	pathcategoryname
	context.categoryname=pathcategoryname
	meta=frappe.db.get_list('Category', fields=['meta_keywords','meta_description'], filters={'route':path.lower()})
	context.MetaKeywords=meta[0].meta_keywords
	context.MetaDescription=meta[0].meta_description
	items=frappe.db.get_all('Item', fields=['route','item_name','brand', 'category'], filters={'category'.lower():pathcategoryname} ,limit_page_length=10)
	context.items = items
	context.banner_image = frappe.db.get_value('Category',
						  fieldname=['banner_image'], filters={'route':path.lower()})
	Brands=frappe.db.get_list('Item Brand Category', filters = {'category': pathcategoryname}, fields=['parent'])	
	context.brand=Brands
	for x in Brands:
		x.route = frappe.db.get_value('ItemBrand',fieldname=['route'], filters={'name':x.parent})
		x.brand_name = frappe.db.get_value('ItemBrand',fieldname=['brand_name'], filters={'name':x.parent})
		item_count = frappe.db.get_all("Item", fields=['name'], filters={'brand': x.parent})
		x.count = len(item_count)	
	featured_products=frappe.db.get_all('Item', 
						fields=['item_name','brand','csd_rate','short_description', 'featured_image','route', 'category', 'name'], 
						filters={'is_featured': "yes", 'category': path},limit_page_length=6)
	for Recentitem in featured_products:
		ItemBrand=frappe.db.get_all('ItemBrand', fields=['route','name','brand_name'],filters={'name':Recentitem.brand})
		ItemCategory=frappe.db.get_all('Category', fields=['route','name','category_name'],filters={'name':Recentitem.category})
		Recentitem.BrandUrl=ItemBrand[0].route
		Recentitem.CategoryUrl=ItemCategory[0].route
		Recentitem.current_location = location
		Recentitem.brand_name = frappe.db.get_value('ItemBrand',fieldname=['brand_name'], filters={'name':Recentitem.brand})
		if Recentitem.current_location:
			market_price = frappe.db.get_list('Item Variant Price', 
				fields = ['market_price'], filters = {'item': Recentitem.name, 'city': location})
			if len(market_price) > 0:
				Recentitem.base_market_price = min(market_price)			
			else:
				Recentitem.base_market_price = {'market_price': 'Na'}		
		else:
			market_price = frappe.db.get_list('Item Variant Price', 
				fields = ['market_price'], filters = {'item': Recentitem.name, 'city': 'Delhi'})
			if len(market_price) > 0:
				Recentitem.base_market_price = min(market_price)			
			else:
				Recentitem.base_market_price = {'market_price': 'Na'}    
	context.featured_products = featured_products
	context.LatestNews = LatestNews
	context.Brands = Brands


	

@frappe.whitelist(allow_guest=True)
def get_items(brand_route, category_route):
	brand_name = frappe.db.get_value('ItemBrand',fieldname=['name'], filters={'route':brand_route})
	category_name = frappe.db.get_value('Category',fieldname=['name'], filters={'route':category_route})
	items = frappe.db.get_list('Item',
		fields=['name','route','item_name'],
		filters={'brand': brand_name, 'category': category_name})

	return items

@frappe.whitelist(allow_guest=True)
def get_brand(product_route):
	brand_name = frappe.db.get_value('Item',fieldname=['brand'], filters={'route':product_route})	
	brand_route = frappe.db.get_list('ItemBrand',
		fields=['name','route'],
		filters={'name': brand_name})

	return brand_route