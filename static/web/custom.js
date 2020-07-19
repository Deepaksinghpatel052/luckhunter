$(document).ready(function(){


var geturl = window.location.href;
var url_in_array = geturl.split("/");
var page_name = "";

console.log();
console.log();

if(base_url==geturl)
{
	$(".page_Home").addClass("active");
	page_name = "Home";
}

if(jQuery.inArray("products", url_in_array) != -1)
{
	$(".page_Products").addClass("active");
	page_name = "Products";
}
if(jQuery.inArray("running-bid", url_in_array) != -1)
{
	$(".page_Running").addClass("active");
	page_name = "Running-bid";
}

if(jQuery.inArray("this-month-bid", url_in_array) != -1)
{
	$(".page_This_Month").addClass("active");
	page_name = "This-Month-bid";
}

if(jQuery.inArray("winners", url_in_array) != -1)
{
	$(".page_Winners").addClass("active");
	page_name = "Winners";
}

if(jQuery.inArray("blog", url_in_array) != -1)
{
	$(".page_Blog").addClass("active");
	page_name = "Blog";
}

if(jQuery.inArray("user", url_in_array) != -1)
{
	$(".page_Account").addClass("active");
	page_name = "Account";
}

if(jQuery.inArray("upcoming-products", url_in_array) != -1)
{
	$(".page_upcoming_product").addClass("active");
	page_name = "Upcoming-product";
}

if(jQuery.inArray("product", url_in_array) != -1)
{
	page_name = $("#get_page_title").val();
}




$.ajax({
   method:"POST",
   url:base_url+"account/system-info",
   dataType:"json",
   success:function(data)
   {

   $("#favicon").attr("href",data.data[0].favicon_icon);
   	$("#show_logo_image").html('<img src="'+data.data[0].Logo+'"  alt="'+data.data[0].Project_name+'">');
   	document.title = page_name+" | "+data.data[0].Title;
   	$("#title_of_footer").text(data.data[0].Title);
   	$("#domein_of_footer").text(data.data[0].Domain);
   	 
   }
});



});