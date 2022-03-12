console.log("{{''|get_livestatus}}");    // this code and function in created in stripe app
var live_mood_status = false;
if('{{''|get_livestatus}}' == '1')
{
  live_mood_status = true;
}


  const pk = new PayKun({ merchantId : "890535565453650", accessToken: "B84C8EB94575AB978A308E83F0E68539", isLive:true});
function initPayment() {
var order_id = $("#set_order_id_for_paykun").val();


$.ajax({
        url: 'https://luckhunter.in/user/orders/get-order-info',
        data: {"order_id":order_id},
        type: 'POST',
        dataType: 'JSON',
        success: function(response){
        if(response.data.total_payment>0)
        {
var order_id_set =  order_id;
        	 let order = {
          amount: response.data.total_payment.toString(), // Amount to collect
          orderId: order_id.toString()+"-"+(new Date).getTime(),
          productName: "LuckHunter Order",
          customerName: "{{user.first_name}}",
          customerEmail: "{{user.email}}",
          customerMobile: "",
          currency: "INR",
          onSuccess: function (transactionId) {
                        var transaction = pk.getTransactionDetail(transactionId, function(transaction) {
                console.log(transaction)
        swal('Payment is success, Your transaction ID : ' + transactionId, {
                  icon: "success",
                    }).then((value) => {


                       $.ajax({
                method:"POST",
                url:"https://luckhunter.in/stripe-payment/update-order-status",
                data: {"order_id":order_id_set,"trans_id":transactionId},
                datraType:"JSON",
                success:function(data)
                {

                 window.location.href = "https://luckhunter.in/user/wallet";

                }
             });

                  });


              });
          },
          onCancelled: function (transactionId) {
              var transaction = pk.getTransactionDetail(transactionId, function(transaction) {
                  swal('Payment is cancelled, Your transaction ID : ' + transaction.transaction.payment_id, {
                  icon: "error",
                    });
              });
          }
	      };
	      //Init Paykun Payment and open checkout popup
	      pk.init(order);
        }
		  }
		});






  }


  function pay_with_paykun(order_id)
  {


$.ajax({
        url: 'https://luckhunter.in/user/orders/get-order-info',
        data: {"order_id":order_id},
        type: 'POST',
        dataType: 'JSON',
        success: function(response){
        if(response.data.total_payment>0)
        {

         initPayment();

			}
        	else
        	{
        		 swal("Subscription successfull.", {
                  icon: "success",
                    }).then((value) => {
                   window.location.href = "{{BASE_URL}}dashboard/";
                  });
        	}
		}
   });


  }
