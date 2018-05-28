
function getCookie(name)
{
var re = new RegExp(name + "=([^;]+)");
var value = re.exec(document.cookie);
return (value != null) ? unescape(value[1]) : null;
}
 
 $( document ).ready(function() {


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

