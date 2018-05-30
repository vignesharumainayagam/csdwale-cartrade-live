from __future__ import unicode_literals
# import frappe
# from _future_ import unicode_literals
import frappe
import frappe.utils
from frappe.utils.oauth import get_oauth2_authorize_url, get_oauth_keys, login_via_oauth2, login_via_oauth2_id_token, login_oauth_user as _login_oauth_user, redirect_post_login
import json
from frappe import _




def get_context(context):
	path = frappe.local.request.path

	context.path = path

	path = path.strip('/')

	word = path.split('/')

	category_route = word[2]

	context.city_route = word[1]

	context.category_route = category_route

	category_name = frappe.db.get_value("Category", 
				 filters={'route': category_route}, fieldname=['name'])

	context.brands1 = frappe.db.get_list('ItemBrand', 
					 filters={'category': category_name,'published':1},
					 fields=['brand_name', 'route', 'name'],order_by='brand_name')