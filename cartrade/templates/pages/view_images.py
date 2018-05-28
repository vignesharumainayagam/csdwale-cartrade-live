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
	path = frappe.local.request.path

	context.path = path

	path = path.replace('csd-', '')

	path = path.strip('/')

	word = path.split('/')

	brand_route = word[1]

	category_route = word[0]

	item_route = word[2]	


	brand_name = frappe.db.get_value("ItemBrand", 
				 filters={'route': brand_route}, fieldname=['brand_name'])

	category_name = frappe.db.get_value("Category", 
				 filters={'route': category_route}, fieldname=['category_name'])

	item_name = frappe.db.get_value("Item", 
				 filters={'route': item_route}, fieldname=['item_name'])

	item_doc_name = frappe.db.get_value("Item", 
				 filters={'route': item_route}, fieldname=['name'])

	context.item_featured_image = frappe.db.get_value("Item", 
				 filters={'route': item_route}, fieldname=['featured_image'])
	

	context.category_route    = category_route
	context.brand_route  = brand_route
	context.item_route  = item_route

	context.brand_name = brand_name	
	context.category_name = category_name	
	context.item_name = item_name	
	context.item_doc_name = item_doc_name
	context.images = frappe.db.get_list('ItemGallery',
					 filters={'parent': item_doc_name},
					 fields=['image','sort_order'],
					 order_by='sort_order')
	context.videos = frappe.db.get_list('VideoGallery',
					 filters={'parent': item_doc_name},
					 fields=['youtube_url','sort_order'],
					 order_by='sort_order')
