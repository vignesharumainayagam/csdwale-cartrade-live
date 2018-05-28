
from __future__ import unicode_literals
# import frappe
# from _future_ import unicode_literals
import frappe
import frappe.utils
import json
from frappe import _


def get_context(context):
	path = frappe.local.request.path
	context.path = path
	word = path.split('/')

	news_route = word[2]

	context.news = frappe.db.get_list("News", fields=['title', 'description', 'image', 'category'], filters={'route': news_route})[0]