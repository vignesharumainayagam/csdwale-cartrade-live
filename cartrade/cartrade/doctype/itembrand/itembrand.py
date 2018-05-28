# -*- coding: utf-8 -*-
# Copyright (c) 2018, Tridots Tech Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.website.website_generator import WebsiteGenerator

class ItemBrand(WebsiteGenerator):

	def validate(self):
		if ' ' in self.brand_name:
			self.route = self.brand_name.replace(" ", "-").lower()
		elif ' ' not in self.brand_name:
			self.route = self.brand_name.lower()	