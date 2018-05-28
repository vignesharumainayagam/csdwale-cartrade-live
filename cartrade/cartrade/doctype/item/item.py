# -*- coding: utf-8 -*-
# Copyright (c) 2018, Tridots Tech Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.website.website_generator import WebsiteGenerator
from frappe import _

# subclass from WebsiteGenerator, not Document
class Item(WebsiteGenerator):
    website = frappe._dict(
        condition_field = "is_published",
        page_title_field = "item_name",
    )

    def get_context(self, context):
        # show breadcrumbs
        context.parents = "cars"
