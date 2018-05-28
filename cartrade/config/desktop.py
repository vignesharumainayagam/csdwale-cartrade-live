# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "Cartrade",
			"color": "grey",
			"icon": "octicon octicon-dashboard",
			"type": "module",
			"label": _("Cartrade")
		},
		{
			"module_name": 'City',
			"type": 'list',
			"label": 'City',
			"_label": _('City'),
			"_id": 'City',
			"_doctype": 'Communication',
			"icon": 'fa fa-envelope-o',
			"color": '#589494',
			"link": 'List/City/List'
		},
	]
