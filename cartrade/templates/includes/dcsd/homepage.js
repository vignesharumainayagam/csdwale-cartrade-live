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
         
                var selected_category = $('#select_category option:selected').val()
                if (selected_category == '0')
                    selected_category = '';
                $.ajax({
                    method: "POST",
                    url: '/',
                    headers: {
                        Accept: "application/json, text/javascript, */*; q=0.01",
                        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
                    },
                    data: {
                        cmd: "frappe.utils.global_search.csd_search",
                        category: selected_category,
                        start: 0,
                        text: request.term,
                        limit: 8,
                        doctype: 'Item'
                    },
                    success: function(data) {
                        console.log(data)
                    }
                })

            },
            minLength: 2,
            select: function(event, ui) {
                console.log(ui);
                location.href = "/" + ui.item.route
            }
        });



    });

