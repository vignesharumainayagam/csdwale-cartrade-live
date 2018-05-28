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
from frappe.utils import nowdate


def get_context(context):
	location = frappe.request.cookies.get('city_location')

	path = frappe.local.request.path

	context.path = path

	path = path.strip('/')

	word = path.split('/')

	city_route = word[1] 

	category_route = word[2] 

	brand_route = word[3] 

	context.city_route = city_route

	context.category_route = category_route

	context.brand_route = brand_route

	brand_name = frappe.db.get_value("ItemBrand", 
				 filters={'route': brand_route}, fieldname=['brand_name'])

	brand_doc_name = frappe.db.get_value("ItemBrand", 
				 filters={'route': brand_route}, fieldname=['name'])

	context.brand_name = brand_name


	category_name = frappe.db.get_value("Category", 
				 filters={'route': category_route}, fieldname=['category_name'])

	category_doc_name = frappe.db.get_value("Category", 
				 filters={'route': category_route}, fieldname=['name'])

	context.category_name = category_name

	city_name = frappe.db.get_value("City", 
				 filters={'route': city_route}, fieldname=['city_name'])

	city_doc_name = frappe.db.get_value("City", 
				 filters={'route': city_route}, fieldname=['name'])

	context.city_name = city_name

	context.dealers = frappe.db.get_list('Dealers',
					  filters = {'city': city_doc_name, 'brand': brand_doc_name},
					  fields= ['route', 'dealer_name', 'dealer_address', 'dealer_phone', 'name'],	
					  order_by='dealer_name',limit_page_length=15)

	context.item_list = frappe.db.get_list('Item', filters={'brand':brand_doc_name}, 
						fields=['item_name','name','route'])
	context.brand_doc_name=brand_doc_name
	context.city_doc_name=city_doc_name

@frappe.whitelist(allow_guest=True)
def inset_to_table(cust_name,cust_email,cust_mob,dealer_int,item):
	sle_dict = {
			'doctype'					: 'Contact Form',
			'customer_name'				: cust_name,
			'customer_mobile_number'	: cust_mob,
			'dealer_intrested'	 		: dealer_int,
			'customer_email_id'			: cust_email,
			'date_submitted'			: nowdate(),
			'item_intrested':item
		}
	sle_doc = frappe.get_doc(sle_dict)
	sle_doc.insert()

@frappe.whitelist(allow_guest=True)
def get_dealers_list(city,brand,page):
	length=(int(page))*15
	Dealers = frappe.db.get_all('Dealers', 
		fields=['route', 'dealer_name', 'dealer_address', 'dealer_phone', 'name'],
		filters={'city': city, 'brand': brand},
		order_by='dealer_name',
		limit_start=length,limit_page_length=15)
	return Dealers