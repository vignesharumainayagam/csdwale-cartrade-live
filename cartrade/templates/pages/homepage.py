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

	LatestNews=frappe.db.get_all('News', fields=['title','description','image','category', 'route'],limit_page_length=6)


	recent_products = frappe.db.get_list('Item', 
		fields=['item_name','category','route','featured_image','short_description','brand', 'name'],
		filters={'is_published':1},limit_page_length=15)

	for x in recent_products:
		x.current_location = frappe.request.cookies.get('city_location')

		x.brand_route = frappe.db.get_value('ItemBrand',
				fieldname=['route'], filters={'name':x.brand})
		x.category_route = frappe.db.get_value('Category',
				fieldname=['route'], filters={'name':x.category})

		x.brand_name = frappe.db.get_value('ItemBrand',
				fieldname=['brand_name'], filters={'name':x.brand})



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



	
	Categories=frappe.db.get_all('Category', fields=['category_name','route','name'],filters={'published':1},order_by='category_name')


	for j in Categories:
		j.brands = frappe.db.get_list('Item Brand Category', filters = {'category': j.name}, fields=['parent'])	
		for f in j.brands:
			f.brand_route = frappe.db.get_value('ItemBrand', fieldname=['route'], filters={'name':f.parent})
			f.brand_name = frappe.db.get_value('ItemBrand', fieldname=['brand_name'], filters={'name':f.parent})
			item_count = frappe.db.get_all("Item", fields=['name'], filters={'brand': f.parent})
			f.count = len(item_count)		

	context.category = Categories		
	context.RecentProducts = recent_products
	context.LatestNews = LatestNews
