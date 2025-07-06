(function($) {
	"use strict"

	// Mobile Nav toggle
	$('.menu-toggle > a').on('click', function (e) {
		e.preventDefault();
		$('#responsive-nav').toggleClass('active');
	})

	// Fix cart dropdown from closing
	$('.cart-dropdown').on('click', function (e) {
		e.stopPropagation();
	});

  // Add to cart functionality
  $('.add-to-cart-btn').on('click',  function(e) {
    e.preventDefault();
    var product_id = $(this).data('product_id');
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    var qty = $('#quantity-input').val() || 1;
    
    if (qty < 2) {
      var qty = $('#quantity-input' + product_id).val() || 1;
    }
    $.ajax({
        type: 'POST',
        url: '/add_to_cart/' + product_id,
        data: {
            product_id: product_id,
            qty : qty,
            csrfmiddlewaretoken: csrf_token
        },
        success: function(data) {
            alertify.set('notifier','position', 'top-right');
            alertify.success(data.msg);
            $('#qty_small').html(data.qty + 'Item(s) selected');
            $('.qty_cart').html(data.qty);
            $('#total_price').html('TOTAL PRICE: $'+ data.total_price)
        },
        error: function() {
            alertify.set('notifier','position', 'top-right');
            alertify.error('Error adding product to cart');
        }
    });
});

// update cart functionality
$('.data_update').on('click', function(e) {
    e.preventDefault();
    var product_id = $(this).data('index');
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    var qty = $('#select'+ product_id).val() || 1;
    console.log(qty);
    $.ajax({
        type: 'POST',
        url: '/update_cart/' + product_id,
        data: {
            product_id: product_id,
            qty : qty,
            csrfmiddlewaretoken: csrf_token
        },
        success: function(data) {
            alertify.set('notifier','position', 'top-right');
            alertify.success(data.msg);
            $('#qty_small').html(data.qty + 'Item(s) selected');
            $('.qty_cart').html(data.qty);
            $('#total_price').html('TOTAL PRICE: $'+ data.total_price)
            $('#total').html('TOTAL: $'+ data.total_price)
        },
        error: function() {
            alertify.set('notifier','position', 'top-right');
            alertify.error('Error updating product to cart');
        }
    });
});



})(jQuery);
