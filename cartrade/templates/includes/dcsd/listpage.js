
$(document).ready(function() {
    $(window).scroll(function() {
        if ($(window).scrollTop() + $(window).height() == $(document).height()) {
            var path = window.location.pathname.replace("/", "");
            var path = path.split("/");
            var brand = path[1].toLocaleLowerCase();
            var category = path[0].split('-')[1].toLocaleLowerCase();

            frappe.call({
                method: "cartrade.templates.pages.listpage.get_more_items",
                args: {
                    brand_route: brand,
                    category_route: category
                },
                callback: function(r) {
                    console.log(r.message)

                //     for (var i = 0; i < r.message.length; i++) {
                //             $('#item_list').append("<section class='b-goods-1'> <div class='row'> <div class='b-goods-1__img'>\
                // <a href='/csd-" + r.message[i].CategoryUrl + "/" + r.message[i].BrandUrl + "/" + r.message[i].route + "'src='/files/lml-freedom-ls-standard-466dd03e5.jpg' alt='/files/lml-freedom-ls-standard-466dd03e5.jpg' style=''> </a> </div> <div class='b-goods-1__inner'> <div class='b-goods-1__header' style='    margin-bottom: 5px;'><span class='b-goods-1__price hidden-th'><span style='font-family: 'Hind';'>₹ </span> 130000.0 </span><a class='b-goods-1__choose hidden-th' href='listing.html'></a> <h2 class='b-goods-1__name' style='font-weight: 500;     text-transform: capitalize;font-size: 15px;    margin-top: 13px;'><a href='/csd-bikes/lml/freedom-ls'>LML FREEDOM LS </a></h2> </div> <span class='b-goods-1__price_th text-primary visible-th'><span style='font-family: 'Hind';'>₹ </span> 130000.0 <a class='b-goods-1__choose' href='listing.html'></a> </span> </div> </div> </section>");
                //         }


                }
            })
        }
    });
});
