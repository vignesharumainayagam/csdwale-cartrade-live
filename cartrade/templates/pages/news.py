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
	News=frappe.db.get_all('News',
			fields=['title','route','description','image','category'],
			limit_page_length=15)
	context.News=News

@frappe.whitelist(allow_guest=True)
def get_news_list(page):
	length=(int(page))*15
	News = frappe.db.get_all('News', 
		fields=['title','route','description','image','category'],		
		limit_start=length,limit_page_length=15)
	return News