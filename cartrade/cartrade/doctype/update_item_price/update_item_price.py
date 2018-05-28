# -*- coding: utf-8 -*-
# Copyright (c) 2018, Tridots Tech Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _, msgprint, scrub

class UpdateItemPrice(Document):

	def on_update(self):
		self.location = None
		self.category = None
		self.brand = None
		frappe.db.sql("""delete from `tabUpdate Item Price Child`;""")
		
	def onload(self):
		self.location = None
		self.category = None
		self.brand = None
		

	def validate(self):
		for x in self.table_7:
			if not x.market_price:
				x.market_price=0
			if not x.price:
				x.price=0
			if x.price_name:
				frappe.db.set_value("Item Variant Price", x.price_name, "csd_price", x.price)
				frappe.db.set_value("Item Variant Price", x.price_name, "market_price", x.market_price)
				frappe.db.set_value("Item Variant Price", x.price_name, "difference", x.market_price-x.price)

			elif not x.price_name:
				frappe.get_doc({
				"doctype": "Item Variant Price",
				"city": x.city,
				"variant": x.variant_name,
				"csd_price": x.price,
				"market_price": x.market_price,
				"item": x.item,
				"difference":x.market_price-x.price
				}).insert()	

	
@frappe.whitelist()
def get_all_data_by_category(category, city):
	variants = frappe.db.get_list('Item Variant', fields=['item', 'brand', 'variant_name', 'name'], filters={'category': category})
	for x in variants:
		x.variant_price = frappe.db.get_value('Item Variant Price',
						  fieldname=['csd_price'], filters={'city': city, 'variant': x.name, 'item': x.item})
		x.variant_market_price = frappe.db.get_value('Item Variant Price',
						  fieldname=['market_price'], filters={'city': city, 'variant': x.name, 'item': x.item})
		x.difference = frappe.db.get_value('Item Variant Price',
						  fieldname=['difference'], filters={'city': city, 'variant': x.name, 'item': x.item})
		x.price_name = frappe.db.get_value('Item Variant Price',
						  fieldname=['name'], filters={'city': city, 'variant': x.name, 'item': x.item})		

	return variants	
	

@frappe.whitelist()
def get_all_data_by_brand(category, city, brand):
	variants = frappe.db.get_list('Item Variant', fields=['item', 'brand', 'variant_name', 'name'], filters={'category': category, 'brand': brand})
	for x in variants:
		x.variant_price = frappe.db.get_value('Item Variant Price',
						  fieldname=['csd_price'], filters={'city': city, 'variant': x.name, 'item': x.item})
		x.variant_market_price = frappe.db.get_value('Item Variant Price',
						  fieldname=['market_price'], filters={'city': city, 'variant': x.name, 'item': x.item})
		x.difference = frappe.db.get_value('Item Variant Price',
						  fieldname=['difference'], filters={'city': city, 'variant': x.name, 'item': x.item})
		x.price_name = frappe.db.get_value('Item Variant Price',
						  fieldname=['name'], filters={'city': city, 'variant': x.name, 'item': x.item})		

	return variants	
	




