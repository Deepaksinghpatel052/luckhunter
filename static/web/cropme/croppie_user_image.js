 $(document).ready(function(){


  $image_crop = $('#image_demo_edit').croppie({

    enableExif: true,

    viewport: {

      width:200,

      height:200,

      type:'square' 

    },

    boundary:{

      width:400,

      height:400

    }

  });


  $('#id_Image').on('change', function(){

var set_status = true;
    var reader = new FileReader();

    reader.onload = function (event) {
      
        var image = new Image();
         image.src = event.target.result;
         //Validate the File Height and Width.
         image.onload = function () {
           var height = this.height;
           var width = this.width;

            if(height >= 200 && width >= 200)
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
            alert("Please select image grater that 300*169px");
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

 // alert(base_url+"user/my-profile/update-image");
           
console.log(response);
             $.ajax({
                method:"POST",
               url:base_url+"user/my-profile/update-image",
               data:{"image":response},
               dataTyep:"html",
               success:function(data)
               {
         
                  window.location.href = base_url+"user/my-profile";
               }
    });

          $('#uploadimageModal_edit').modal('hide');

    })

  });



});
