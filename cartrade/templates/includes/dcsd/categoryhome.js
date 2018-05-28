$(document).ready(function() {
    $('#select_brand').change(function() {
        var brand = $('#select_brand option:selected').val();

        frappe.call({
            method: "cartrade.templates.pages.categoryhome.get_items",
            args: {
                brand_route: brand,
                category_route: window.location.pathname.replace('/', '').split('-')[1]
            },
            callback: function(r) {
                $('#select_item').html('');
                console.log(r.message)
                if (r.message != undefined) {
                    for (var i = 0; i < r.message.length; i++) {
                        $('#select_item').append('<option value=' + r.message[i].route + '>' + r.message[i].item_name + '</option>');
                    }
                } else {
                    $('#select_item').html('<option value="0">Select Product</option>');
                }
            }
        });

    });

    // $('#search_item').click(function() {
    //     var s_brand = $('#select_brand option:selected').val();
    //     var s_item = $('#select_item option:selected').val();
    //     console.log(s_brand)
    //     console.log(s_item)
    //     if (s_brand != "0" && s_item != "0") {
    //         window.location.replace(window.location.href + '/' + s_brand + '/' + s_item)
    //     } else if (s_brand != "0" && s_item == "0") {
    //         window.location.replace(window.location.href + '/' + s_brand)
    //     } else {
    //         frappe.call({
    //         method: "cartrade.templates.pages.categoryhome.get_brand",
    //         args: {
    //             product_route: s_item                
    //         },
    //         callback: function(r) {                
    //             window.location.replace(window.location.href+'/'+r.message[0].route+'/'+s_item)        
    //         }
    //     });
    //     }
    // });
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
            // var user = getCookie("user_id");
            var selected_category = $('#category_name').val()
            $.ajax({
                method: "POST",
                url: '/',
                headers: {
                    Accept: "application/json, text/javascript, */*; q=0.01",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
                },
                data: {
                    cmd: "frappe.utils.global_search.web_search",
                    start: 0,
                    text: request.term,
                    limit: 8,
                    doctype: 'Item'
                },
                success: function(data) {
                    var bty = []
                    $.each(data.message, function(index, item) {
                        var parts = item.content;
                        var part = parts.split('|||')
                        if (part.length > 3) {
                            var category = part[2].split(':')[1];
                            console.log(category)
                            console.log(selected_category)
                            if (selected_category == category.trim()) {
                                var brand = part[1].split(':')[1].replace('-', '')
                                var url = 'csd-' + category + '/' + brand + '/';
                                var rr = brand.replace(/-/g, '') + '-' + category + '/';
                                var route = url.replace(/ /g, '');
                                bty.push({
                                    label: part[1].split(':')[1] + item.title,
                                    value: item.title,
                                    content: item.content,
                                    route: route + item.route || ''
                                })
                            }
                        }

                    })
                    response(bty)

                }
            })

        },
        minLength: 2,
        select: function(event, ui) {
            console.log(ui);
            location.href = "/" + ui.item.route
        }
    });

    $('#find_dealers').click(function() {
        $('#myModal1').modal('show');
        $("#myModal1").prepend('<div class="modal-backdrop fade in" style="height: 100%;"></div>');
    })

    $('#search_Bike').click(function() {
        $('#myModal123').modal('show');
        $("#myModal123").prepend('<div class="modal-backdrop fade in" style="height: 100%;"></div>');
    })

    $('#modalbrand').change(function() {
        var selected_brand = $('#modalbrand option:selected').val();

        frappe.call({
            method: "cartrade.templates.pages.categoryhome.get_items",
            args: {
                brand_route: selected_brand,
                category_route: window.location.pathname.replace('/', '').split('-')[1]
            },
            callback: function(r) {
                $('#modalitem').html('');
                for (var i = 0; i < r.message.length; i++) {
                    $('#modalitem').append('<option value=' + r.message[i].route + '>' + r.message[i].item_name + '</option>');
                }
                $('.selectpicker').selectpicker('refresh');

                console.log(r.message)
            }
        });
    })

    $('#get_dealers').click(function() {
        var category_route = window.location.pathname.replace('/', '').split('-')[1]
        var brand_route = $('#modalbrand option:selected').val();
        var city_route = $('#modalcity option:selected').val();
        $("#errMsg").hide();
        if(brand_route!=""&&city_route!="")        
            window.location.replace('csd-dealers/' + city_route + '/' + category_route + '/' + brand_route)
        else{
            if(city_route!=""&&brand_route==""){
                window.location.replace('csd-dealers/' + city_route + '/' + category_route)
            }else{
               $("#errMsg").show();
            }
        }
    })
});