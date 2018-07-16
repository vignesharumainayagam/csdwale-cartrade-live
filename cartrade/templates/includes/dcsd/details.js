
function getCookie(name)
{
var re = new RegExp(name + "=([^;]+)");
var value = re.exec(document.cookie);
return (value != null) ? unescape(value[1]) : null;
}
 
function openPopup(name, dealer_name) {
    $('#contactdealer').modal('show');
    $("#contactdealer").prepend('<div class="modal-backdrop fade in" style="height: 100%;"></div>');
    dealername = name;
    $("#contactdealer #dealersName").text('Contact ' + dealer_name)
    $("#fname_err").hide();
    $("#phone_err").hide();
    $("#email_err").hide();
    $("#model_err").hide();
    $("#emailValid_err").hide();
    $('#cust_name').val('');
    $('#cust_email').val('');
    $('#cust_mob').val('');
} 
 $( document ).ready(function() {
    $("#cust_mob").keydown(function(e) {
        KeyDown(e);
    });
    $('#submit').click(function() {
        var cust_name = $('#cust_name').val();
        var cust_email = $('#cust_email').val();
        var cust_mob = $('#cust_mob').val();
        var item = $("#item").val();
        var validEmail = ValidateEmail(cust_email)
        $("#fname_err").hide();
        $("#phone_err").hide();
        $("#email_err").hide();
        $("#model_err").hide();
        $("#emailValid_err").hide();
        if (cust_mob != "" && cust_email != "" && cust_name != "" && item != "0" && validEmail == true) {
            frappe.call({
                method: "cartrade.templates.pages.dealers_list.inset_to_table",
                args: {
                    cust_name: cust_name,
                    cust_email: cust_email,
                    cust_mob: cust_mob,
                    dealer_int: dealername,
                    item: item
                },
                callback: function(r) {
                    $('#contactdealer').modal('hide');
                    alert("The Dealer Will Get Back to You Soon")
                }
            });
        } else {
            if (cust_name == "")
                $("#fname_err").show();
            if (cust_mob == "")
                $("#phone_err").show();
            if (item == "0")
                $("#model_err").show();
            if (cust_email == "") {
                $("#email_err").show();
            } else if (validEmail == false) {
                $("#emailValid_err").show();
            }
        }
    });

function ValidateEmail(email) {
    var expr = /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/;
    return expr.test(email);
};
function KeyDown(e) {
    if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 190]) !== -1 ||
        (e.keyCode === 65 && (e.ctrlKey === true || e.metaKey === true)) ||
        (e.keyCode >= 35 && e.keyCode <= 40)) {
        return;
    }
    if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
        e.preventDefault();
    }
}

    $("#select_variant").change(function(){
    var market_price = $('#select_variant option:selected').attr('data-market-price');
    var csd_price = $('#select_variant option:selected').attr('data-csd-price');  
         
    $('#market_price').html(market_price);
    $('#csd_price').html(csd_price);
    
    var a = $('#market_price').html();
    var b = $('#csd_price').html();
    a = a.trim();
    b = b.trim();
    a = parseFloat(a);
    b = parseFloat(b);

    var c = a - b;
    $('#difference').html(parseFloat(c));
    });

    $("#select_location").change(function() {

    var city = $("#select_location option:selected").val();
    $.removeCookie("city_location");
    $.cookie("city_location", city, { path: '/' });
    location.reload();
    });






var location_city = getCookie("city_location")
if(location_city){ 
$('#select_location').selectpicker('val', location_city);   
}
else{
$('#select_location').selectpicker('val', 'Delhi');
} 

var a = $('#market_price').html();
var b = $('#csd_price').html();
a = a.trim();
b = b.trim();
a = parseFloat(a);
b = parseFloat(b);

var c = a - b;
$('#difference').html(parseFloat(c));


});

