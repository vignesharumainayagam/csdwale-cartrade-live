from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Masters"),
			"items": [
				{
					"type": "doctype",
					"name": "City",
				},
				{
					"type": "doctype",
					"name": "Category",
					"icon": 'fa fa-envelope-o',
				},
				{
					"type": "doctype",
					"name": "Car Manufacturers",
				},
				{
					"type": "doctype",
					"name": "ItemBrand",
					"label": "Item Brands",
				},
				{
					"type": "doctype",
					"name": "Update Item Price"
				},
				
			]
		},
		{
			"label": _("Items"),
			"items": [
				{
					"type": "doctype",
					"name": "Item",
					"label": "Item",
				},
				{
					"type": "doctype",
					"name": "Item Variant",
					"label": "Item Variant",
				},
				{
					"type": "doctype",
					"name": "Specification",
					"label": "Specification",
				},
				{
					"type": "doctype",
					"name": "ItemGallery",
					"label": "Item Gallery",
				},
				{
					"type": "doctype",
					"name": "VideoGallery",
					"label": "Video Gallery",
				},

				

			]
		},
		{
			"label": _("Others"),
			"items": [
				{
					"type": "doctype",
					"name": "News",
					"label": "News",
				},
				{
					"type": "doctype",
					"name": "Dealers",
					"label": "Dealers",
				},
				{
					"type": "doctype",
					"name": "Custom Page",
					"label": "Custom Page",
				},
				{
					"type": "doctype",
					"name": "Contact Form",
					"label": "Contact Form",
				},

			]
		}
	]
