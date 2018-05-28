from __future__ import unicode_literals
# import frappe
# from _future_ import unicode_literals
import frappe
import frappe.utils
from frappe.utils.oauth import get_oauth2_authorize_url, get_oauth_keys, login_via_oauth2, login_via_oauth2_id_token, login_oauth_user as _login_oauth_user, redirect_post_login
import json
from frappe import _




def get_context(context):
	context.category = frappe.db.get_list('Category', 
						fields=['category_name', 'route'],
						filters={'published':1},order_by='category_name')
	path = frappe.local.request.path

	context.path = path

	path = path.strip('/')

	word = path.split('/')

	context.city_route = word[1]