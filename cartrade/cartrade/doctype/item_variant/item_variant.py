# -*- coding: utf-8 -*-
# Copyright (c) 2018, Tridots Tech Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.model.naming import make_autoname


class ItemVariant(WebsiteGenerator):
    website = frappe._dict(
        condition_field = "is_published",
        page_title_field = "variant_name",
    )

    def get_context(self, context):
        # show breadcrumbs
        context.parents = "cars"

    def autoname(self):
    	self.name = make_autoname('variant.######')  
    
    def on_update(self):
        if not self.route and self.is_published == 1:
            self.route = self.variant_name.replace(" ", "-").lower()   