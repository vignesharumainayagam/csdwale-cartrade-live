// Copyright (c) 2018, Tridots Tech Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Update Item Price', {
    
    after_save: function(frm) {
        cur_frm.reload_doc();
        frappe.set_route("modules", "Cartrade")
    },
    get_items: function(frm) {
        if (frm.doc.location) {
            if (frm.doc.category) {                
                if (frm.doc.brand) {
                    frappe.call({
                        method: "cartrade.cartrade.doctype.update_item_price.update_item_price.get_all_data_by_brand",
                        args: {
                            category: frm.doc.category,
                            city: frm.doc.location,
                            brand: frm.doc.brand
                        },
                        callback: function(r) {
                            frm.doc.table_7=[]
                            for (var e = frm.doc.table_7.length; e < r.message.length; e++) {
                                frappe.model.add_child(cur_frm.doc, "Update Item Price Child", "table_7");
                                $.each(frm.doc.table_7 || [], function(e, v) {
                                    frappe.model.set_value(v.doctype, v.name, "item", r.message[e].item)
                                    frappe.model.set_value(v.doctype, v.name, "variants", r.message[e].variant_name)
                                    frappe.model.set_value(v.doctype, v.name, "price", r.message[e].variant_price)
                                    frappe.model.set_value(v.doctype, v.name, "variant_name", r.message[e].name)
                                    frappe.model.set_value(v.doctype, v.name, "city", frm.doc.location)
                                    frappe.model.set_value(v.doctype, v.name, "changed", 0)
                                    frappe.model.set_value(v.doctype, v.name, "price_name", r.message[e].price_name)
                                    frappe.model.set_value(v.doctype, v.name, "market_price", r.message[e].variant_market_price)



                                })
                                frm.refresh_field("table_7");
                            }
                        }
                    });
                } else {
                    frappe.call({
                        method: "cartrade.cartrade.doctype.update_item_price.update_item_price.get_all_data_by_category",
                        args: {
                            category: frm.doc.category,
                            city: frm.doc.location,
                        },
                        callback: function(r) {
                            frm.doc.table_7=[]
                            for (var e = frm.doc.table_7.length; e < r.message.length; e++) {
                                frappe.model.add_child(cur_frm.doc, "Update Item Price Child", "table_7");
                                $.each(frm.doc.table_7 || [], function(e, v) {
                                    frappe.model.set_value(v.doctype, v.name, "item", r.message[e].item)
                                    frappe.model.set_value(v.doctype, v.name, "variants", r.message[e].variant_name)
                                    frappe.model.set_value(v.doctype, v.name, "price", r.message[e].variant_price)
                                    frappe.model.set_value(v.doctype, v.name, "variant_name", r.message[e].name)
                                    frappe.model.set_value(v.doctype, v.name, "city", frm.doc.location)
                                    frappe.model.set_value(v.doctype, v.name, "changed", 0)
                                    frappe.model.set_value(v.doctype, v.name, "price_name", r.message[e].price_name)
                                    frappe.model.set_value(v.doctype, v.name, "market_price", r.message[e].variant_market_price)

                                })
                                frm.refresh_field("table_7");
                            }
                        }
                    });
                }
            } else {
                frappe.msgprint(__("No category has been selected"))
            }
        } else {
            frappe.msgprint(__("No location has been selected"))
        }
    }

});

frappe.ui.form.on("Update Item Price", "refresh", function(frm) {

    frm.set_query("brand", function() {
        return {
            "filters": {
                "category": frm.doc.category
            }
        };
    });
});