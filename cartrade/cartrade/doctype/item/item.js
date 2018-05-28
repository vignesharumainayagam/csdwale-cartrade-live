// Copyright (c) 2018, Tridots Tech Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Item', {
	refresh: function(frm) {
		frm.set_query("brand", function() {
        return {
            "filters": {
                "category": frm.doc.category
            }
        };
    });
	}
});
