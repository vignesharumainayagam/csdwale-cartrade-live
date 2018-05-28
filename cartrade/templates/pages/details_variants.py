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


def get_context(context):
	location = frappe.request.cookies.get('city_location')

	path = frappe.local.request.path
	
	path = path.replace('csd-', '')

	path = path.replace('-price', '')

	context.path = path

	path = path.strip('/')

	word = path.split('/')

	category_route = word[0]

	brand_route = word[1]

	item_route = word[2]

	variant_route = word[3]

	item_name = frappe.db.get_value("Item", 
				filters={'route': item_route}, fieldname=['name'])

	context.item_brand = frappe.db.get_value("ItemBrand", 
						 filters={'route': brand_route}, fieldname=['brand_name'])

	context.item_title = frappe.db.get_value("Item", 
						 filters={'route': item_route}, fieldname=['item_name'])

	context.category_title = frappe.db.get_value("Category", 
						 filters={'route': category_route}, fieldname=['category_name'])


	context.item_brand_route = brand_route

	context.item_category_route = category_route

	context.item_route = item_route

	context.variant_route = variant_route


	
	context.variant_title = frappe.db.get_value("Item Variant", 
						 filters={'route': variant_route, 'item': item_name}, fieldname=['variant_name'])

	context.meta_title = frappe.db.get_value("Item Variant", 
						 filters={'route': variant_route, 'item': item_name}, fieldname=['meta_title'])

	context.meta_description = frappe.db.get_value("Item Variant", 
						 filters={'route': variant_route, 'item': item_name}, fieldname=['meta_description'])

	context.meta_keywords = frappe.db.get_value("Item Variant", 
						 filters={'route': variant_route, 'item': item_name}, fieldname=['meta_keywords'])


	context.item_featured_image = frappe.db.get_value("Item", 
				filters={'route': item_route}, fieldname=['featured_image'])

	
	item_variant_doc_name = frappe.db.get_value("Item Variant", 
				filters={'route': variant_route}, fieldname=['name'])

	context.item_variant_doc_name =item_variant_doc_name


	item_variants = frappe.db.get_all("Item Variant",
					fields=['route','variant_name', 'name'],
				    filters={'item': item_name},
				    limit_page_length= 100)

	for x in item_variants:
		if frappe.request.cookies.get('city_location'):


			price = frappe.db.get_list('Item Variant Price', 
				fields = ['market_price', 'csd_price'], 
				filters = {'variant': x.name, 'city': frappe.request.cookies.get('city_location'), 'item': item_name})

			if len(price) > 0:
				x.csd_price = price[0].csd_price
				x.market_price = price[0].market_price
			else:
				x.csd_price = "Na"
				x.market_price = "Na"

		else:
			price = frappe.db.get_list('Item Variant Price', 
				fields = ['market_price', 'csd_price'],
				filters = {'variant': x.name, 'city': 'Delhi', 'item': item_name})

			if len(price) > 0:
				x.csd_price = price[0].csd_price
				x.market_price = price[0].market_price
			else:
				x.csd_price = "Na"
				x.market_price = "Na"
	context.item_variants = item_variants	

	variant_specifications = frappe.db.get_list('Item Specification', 
									 fields=['specification', 'value'],
									 filters={'parent': item_variant_doc_name})

	for x in variant_specifications:
		x.specification_group = frappe.db.get_value("Specification", 
				filters={'name': x.specification}, fieldname=['specification_category'])


	context.variant_specifications = variant_specifications	



	if frappe.request.cookies.get('city_location'):
		price = frappe.db.get_list('Item Variant Price', 
			fields = ['market_price', 'csd_price'], 
			filters = {'variant': item_variant_doc_name, 'city': frappe.request.cookies.get('city_location'), 'item': item_name})
		if len(price) > 0:
			context.csd_price = price[0].csd_price
			context.market_price = price[0].market_price
		else:
			context.csd_price = "Na"
			context.market_price = "Na"
	else:
		price = frappe.db.get_list('Item Variant Price', 
			fields = ['market_price', 'csd_price'], filters = {'variant': item_variant_doc_name, 'city': 'Delhi', 'item': item_name})
		if len(price) > 0:
			context.csd_price = price[0].csd_price
			context.market_price = price[0].market_price
			context.difference=price[0].difference
		else:
			context.csd_price = "Na"
			context.market_price = "Na"