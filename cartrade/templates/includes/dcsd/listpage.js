var itemssss = true;
var num = 0;
$(document).ready(function() {
    $('#get_dealers').click(function() {
        var category_route = window.location.pathname.replace('/', '').replace('csd-','').split('/')[0]
        var brand_route = $('#modalbrand option:selected').val();
        var city_route = $('#modalcity option:selected').val();
        $("#errMsg").hide();
        if(brand_route!=""&&city_route!="")        
            window.location.replace('/csd-dealers/' + city_route + '/' + category_route + '/' + brand_route)
        else{
            if(city_route!=""&&brand_route==""){
                window.location.replace('/csd-dealers/' + city_route + '/' + category_route)
            }else{
               $("#errMsg").show();
            }
        }
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

    $(window).scroll(function() {
        if(itemssss){
        if ($(window).scrollTop()>= 700) {
            var path = window.location.pathname.replace("/", "");
            var path = path.replace('csd-','');
            var path = path.split("/");
            var brand = path[1].toLocaleLowerCase();
            var category = path[0].toLocaleLowerCase();
                    num = num + 20;                
            frappe.call({
                method: "cartrade.templates.pages.listpage.get_more_items",
                async: false,
                args: {
                    brand_route: brand,
                    category_route: category,
                    num:num,

                },
                callback: function(r) {
                    console.log(r.message)

                    if (r.message != undefined) {
                        itemssss = false
                    for (var i = 0; i < r.message.length; i++) {
                        var href_var = "/csd-"+r.message[i].CategoryUrl+"/"+r.message[i].BrandUrl+"/"+r.message[i].route+"";
                        var item_name = r.message[i].brand+" "+r.message[i].item_name;
                        var item_image = '/files/no-img.png';
                        if(r.message[i].featured_image){item_image = r.message[i].featured_image}
                        var item_price = 0;
                        if (parseFloat(r.message[i].base_market_price.market_price) >0)
                            {
                                if (parseFloat(r.message[i].base_market_price.market_price) >= 100000) {
                                    item_price = parseFloat(r.message.base_market_price.market_price) / 100000+'Lakhs' 
                                }
                                if (parseFloat(r.message[i].base_market_price.market_price) >= 10000 && parseFloat(item.base_market_price.market_price) < 100000)
                                {
                                    item_price = parseFloat(r.message[i].base_market_price.market_price) / 10000+'K' 
                                }    
                           }
                        else{ item_price = 'Na' };
                        var follo = '<section class="b-goods-1" style="    "> <div class="row"> <div class="b-goods-1__img" style="    "> <a href='+href_var+'> <img class="img-responsive img-responsive1" src='+item_image+' alt='+item_image+'> </a> </div> <div class="b-goods-1__inner row"> <div class="col-md-7 col-xs-12"> <h2 class="b-goods-1__name" style="font-weight: 500;     text-transform: capitalize;font-size: 15px; margin-top: 13px;"><a href='+href_var+'>'+item_name+'</a></h2> </div> <div class="col-md-5 col-xs-12"> <span class="b-goods-1__price hidden-th"><span style="font-family: Hind;">₹ </span>  Na  </span> <a class="b-goods-1__csdprice hidden-th" href='+href_var+'>CSD Price <i class="fa fa-arrow-right"></i></a> </div> </div> </div> </section>'                 
                            $('#item_list').append(follo);
                        }
                    }


                }
            })
        }
    }
    });
});
