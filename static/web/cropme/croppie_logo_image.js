 $(document).ready(function(){


  $image_crop = $('#image_demo_edit').croppie({

    enableExif: true,

    viewport: {

      width:500,

      height:250,

      type:'square' 

    },

    boundary:{

      width:700,

      height:400

    }

  });


  $('#producer_banner_image').on('change', function(){

var set_status = true;
    var reader = new FileReader();

    reader.onload = function (event) {
      
        var image = new Image();
         image.src = event.target.result;
         //Validate the File Height and Width.
         image.onload = function () {
           var height = this.height;
           var width = this.width;

            if(height >= 250 && width >= 500)
          {
             $image_crop.croppie('bind', {

              url: event.target.result
       
              }).then(function(){

                console.log('jQuery bind complete');

              });
              $('#uploadimageModal_edit').modal('show');
          }
          else
          {
            set_status = false;
            alert("Please select image grater that 500*250px");
          }
         }

     

    }


  if(set_status)
  {
    reader.readAsDataURL(this.files[0]);

    
  }
    

  });



  $('.crop_image_edit').click(function(event){

$('.crop_image_edit').html('Image Uploading');
$('.crop_image_edit').attr("disabled", true);

    $image_crop.croppie('result', {

      type: 'canvas',

      size: 'viewport'

    }).then(function(response){

$('#show_banner_image').empty();
$('#producer_banner_image_vlue_set').val(response);
$("#show_banner_image").html('<img src="'+response+'"  style="border: 2px solid;" />');
     
$('.crop_image_edit').html('Crop Image');
$('.crop_image_edit').attr("disabled", false);
          $('#uploadimageModal_edit').modal('hide');

    })

  });



});


