$(document).ready(function(){
    //Add to wishlist
    $(".add_to_wishlist").on('click', function(e){
        e.preventDefault();

        var product_id = $(this).attr('data-id');
        var this_val = $(this);
        var url = $(this).attr('data-url');
        var data = {
            id: product_id
        }

        //console.log("Product is: ", product_id);

        $.ajax({
            type:'GET',
            url:url,
            data:data,
            //dataType: 'json',
            success: function(response){
                    console.log(response)
                    if(response.status == 'Login_required'){
                        swal(response.message, "", "info").then(function(){
                            window.location = '/accounts/login';
                        })
                    } else if(response.status == 'Failed'){
                        swal(response.message, "", "error")
                    }else{
                       $("#wishlist_counter").html(response.wishlist_counter['wishlist_count']);
                       swal(response.message, "", "success") 
                    }                   
            }
        });
    });

    //delete to wishlist
    $(".delete_to_wishlist").on('click', function(e){
        e.preventDefault();

        var product_id = $(this).attr('data-id');
        var this_val = $(this);
        var url = $(this).attr('data-url');
        var data = {
            id: product_id
        }

        $.ajax({
            type:'GET',
            url:url,
            data:data,
            success: function(response){
                    console.log(response)
                    if(response.status == 'Login_required'){
                        swal(response.message, "", "info").then(function(){
                            window.location = '/accounts/login';
                        })
                    } else if(response.status == 'Failed'){
                        swal(response.message, "", "error")
                    }else{
                       $("#wishlist_counter").html(response.wishlist_counter['wishlist_count']);
                       swal(response.message, "", "success").then(function(){
                            window.location = '/accounts/user_wishlist';
                        })  
                    }  
            }
        });
    });


});    