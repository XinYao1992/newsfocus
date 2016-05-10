jQuery(document).ready(function() {
    $('.search-form input[type="text"]').on('focus', function() {
    	$(this).removeClass('input-error');
    });

    $('.search-form').on('submit', function(e) {

    	$(this).find('input[type="text"], input[type="password"], textarea').each(function(){
    		if( $(this).val() == "" ) {
    			e.preventDefault();
    			$(this).addClass('input-error');
    		}
    		else {
    			$(this).removeClass('input-error');
    		}
    	});

    });
});
