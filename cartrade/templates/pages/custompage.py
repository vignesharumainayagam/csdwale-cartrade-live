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

	path = path.strip('/')

	word = path.split('/')

	page_route = word[0]

	dat = frappe.db.get_all('Custom Page', fields=['route','text_editor_6', 'page_name'], filters={'route' :page_route})[0]
	context.data = dat