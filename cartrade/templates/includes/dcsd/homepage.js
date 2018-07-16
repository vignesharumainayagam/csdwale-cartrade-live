

    $(function() {
    $.widget("custom.catcomplete", $.ui.autocomplete, {
        _create: function() {
            this._super();
            this.widget().menu("option", "items", "> :not(.ui-autocomplete-category)");
        },
        _renderMenu: function(ul, items) {
            // console.log(items)
            var that = this,
                currentCategory = "";
            $.each(items, function(index, item) {
                var li;
                // if (item.category != currentCategory) {
                //     ul.append("<li class='ui-autocomplete-category'>" + item.category + "</li>");
                //     currentCategory = item.category;
                // }
                li = that._renderItemData(ul, item);
                if (item.category) {
                    li.attr("aria-label", item.category + " : " + item.label);
                }
            });
        }
    });
    $("#search_item").catcomplete({
        delay: 150,
        autoFocus: true,
        source: function(request, response) {

            frappe.call({
                        method: "frappe.utils.global_search.csd_search",
                        args: {
                            start: 0,
                            limit: 10,
                            text: request.term
                        },
                        callback: function(r) {
                            console.log(r)
                            var bty = []
                            $.each(r.message, function(index, item) {
     
                
                                    bty.push({
                                        label: item[2],
                                        value: item[2],
                                        content: item[2],
                                        route: item[1]
                                    })


                            })
                            response(bty)
                        }
                    }); 

        },
        minLength: 2,
        select: function(event, ui) {
            console.log(ui);
            location.href = "/" + ui.item.route
        }
    });



});

