$(document).ready(function(){
        $(".add_to_wishlist").on('click', function(){
                var product_id = $(this).attr("data-id")
                var this_val = $(this)
                console.log("Product is: ", product_id);
        });
});