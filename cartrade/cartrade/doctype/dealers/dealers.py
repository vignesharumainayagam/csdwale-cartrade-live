# -*- coding: utf-8 -*-
# Copyright (c) 2018, Tridots Tech Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.website.website_generator import WebsiteGenerator

class Dealers(WebsiteGenerator):
	website = frappe._dict(
        condition_field = "is_published",
        page_title_field = "dealer_name",
    )

    