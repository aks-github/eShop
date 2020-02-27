function boss_addToCart(product_id) {
  $.ajax({
      url: 'index.php?route=bossthemes/cart/add',
      type: 'post',
      data: 'product_id=' + product_id,
      dataType: 'json',
      success: function(json) {

          if (json['redirect']) {
              location = json['redirect'];
          }

          if (json['error']) {
              if (json['error']['warning']) {
                  addProductNotice(json['title'], json['thumb'], json['error']['warning'], 'failure');
              }
          }

          if (json['success']) {
              addProductNotice(json['title'], json['thumb'], json['success'], 'success');
              $('#cart_menu span.s_grand_total').html(json['total_sum']);
              $('#cart_menu div.s_cart_holder').html(json['output']);
			  $('#cart-total').html(json['total']);
          }
      }
  });
}

function boss_addToWishList(product_id) {
	$.ajax({
		url: 'index.php?route=bossthemes/wishlist/add',
		type: 'post',
		data: 'product_id=' + product_id,
		dataType: 'json',
		success: function(json) {
			if (json['success']) {
				addProductNotice(json['title'], json['thumb'], json['success'], 'success');
			}
			if (json['failure']) {
				addProductNotice(json['title'], json['thumb'], json['failure'], 'failure');
			}
			$('#wishlist-total').html(json['total']);
		}
	});
}

function boss_addToCompare(product_id) {
	$.ajax({
		url: 'index.php?route=bossthemes/compare/add',
		type: 'post',
		data: 'product_id=' + product_id,
		dataType: 'json',
		success: function(json) {
			if (json['success']) {
                addProductNotice(json['title'], json['thumb'], json['success'], 'success');
				$('#compare-total').html(json['total']);
			}
		}
	});
}

function appendNoticeTemplates() {
  if (!$("#notification-container").length) {
    var tpl = '<div id="notification-container" style="display: none">\
                 <div id="thumb-template">\
                   <a class="ui-notify-cross ui-notify-close boss_button_remove" href="javascript:;"></a>\
                   <h2 class="boss_icon_success"><span class="boss_title">#{title}</span></h2>\
                   <div class="boss_text">\
                     #{thumb}\
                     <h3>#{text}</h3>\
                   </div>\
                 </div>\
                 <div id="nothumb-template">\
                   <a class="ui-notify-cross ui-notify-close boss_button_remove" href="javascript:;"></a>\
                   <h2 class="boss_icon_success"><span class="boss_title">#{title}</span></h2>\
                   <div class="boss_text">\
                     <h3>#{text}</h3>\
                   </div>\
                 </div>\
               </div>';
    $(tpl).appendTo("body");
    $("#notification-container").notify();
  }
}

function addProductNotice(title, thumb, text, type) {
    if ($.browser.msie && $.browser.version.substr(0,1) < 8) {
        simpleNotice(title, text, type);

        return false;
    }
    appendNoticeTemplates();
    $("#notification-container").notify("create", "thumb-template", {
        title: title,
        thumb: thumb,
        text:  text,
        type: type
        },{
        expires: 4000
        }
    );
}

function simpleNotice(title, text, type) {
    appendNoticeTemplates();
    $("#notification-container").notify("create", "nothumb-template", {
        title: title,
        text:  text,
        type: type
        },{
        expires: 4000
        }
    );
}




$(document).ready(function() {
	// search
	$('#boss-search input[name=\'filter_name\']').bind('keydown', function(e) {
		if (e.keyCode == 13) {
			$('#boss-button-search').trigger('click');
		}		
	});

	$('#boss-button-search').bind('click', function() {
		//url =  $('base').attr('href') + 'search';
		url = '/search';
		var search = $('#boss-search input[name=\'filter_name\']').attr('value');
		
		if (search) {
			url += '?&search=' + encodeURIComponent(search);
		}

		var category_id = $('#boss-search select[name=\'filter_category_id\']').attr('value');
		
		if (category_id) {
			url += '&category_id=' + encodeURIComponent(category_id);
		}

		location = url;
	});
	
	if(getWidthBrowser() < 768){
		$('#boss_menu_vertical .quick-select p').click(function(){
			if($(this).next().css('display') == 'none'){
				$(this).next().show();
				$('#boss_menu_vertical .quick-select p').addClass('selected');
			}else{
				$(this).next().hide();
				$('#boss_menu_vertical .quick-select p').removeClass('selected');
			}	
		});
	}else{
		// mega menu vertical
		$('#boss_menu_vertical .sub-inside > ul > li > a').hover(function(){ 
			 hover();
		});
	}
});


/* mega boss menu */
$(window).load(function(){
	var menuWidth = 1180;
	var numColumn = 6;
	var currentWidth = $("#boss_menu").outerWidth() + $(".quick-select").outerWidth() - 2;
	// responsive
	if (currentWidth < menuWidth) {
		new_width_column = currentWidth / numColumn;
		$('#boss_menu div.dropdown').each(function(index, element) {
			$(this).width(parseFloat($(this).css("width"))/menuWidth*numColumn * new_width_column);
		});
		$('#boss_menu div.option').each(function(index, element) {
			$(this).width(parseFloat($(this).css("width"))/menuWidth*numColumn * new_width_column);
		});
		$('#boss_menu ul.column').each(function(index, element) {
			$(this).width(parseFloat($(this).css("width"))/menuWidth*numColumn * new_width_column);
		});
	}
	
	$('#boss_menu ul > li > a + div').each(function(index, element) {
		var menu = $('#boss_menu').offset();
		var dropdown = $(this).parent().offset();			
		i = (dropdown.left + $(this).outerWidth()) - (menu.left + $('#boss_menu').outerWidth());
		
		if (i > 0) {
			$(this).css('margin-left', '-' + (i) + 'px');
		}
	});

	// IE6 & IE7 Fixes
	if ($.browser.msie) {
		if ($.browser.version <= 6) {
			$('#column-left + #column-right + #content, #column-left + #content').css('margin-left', '195px');
			
			$('#column-right + #content').css('margin-right', '195px');
		
			$('.box-category ul li a.active + ul').css('display', 'block');	
		}
		
		if ($.browser.version <= 7) {
			$('#boss_menu > ul > li').bind('mouseover', function() {
				$(this).addClass('active');
			});
				
			$('#boss_menu > ul > li').bind('mouseout', function() {
				$(this).removeClass('active');
			});	
		}
	}
});

/* boss mega menu vertical */
$(window).load(function(){
	var menuWidth = 948;
	var numColumn = 6;
	var currentWidth = $("#container").outerWidth() - 20 - $("#boss_menu_vertical").outerWidth()-2;
	//alert(currentWidth);
	// responsive
	if (currentWidth < menuWidth) {
		new_width_column = currentWidth / numColumn;
		$('#boss_menu_vertical div.dropdown').each(function(index, element) {
			if($(this).width() > currentWidth){
				$(this).width(parseFloat($(this).css("width"))/menuWidth*numColumn * new_width_column);
			}
		});
		$('#boss_menu_vertical div.option').each(function(index, element) {
			if($(this).width() > currentWidth){
				$(this).width(parseFloat($(this).css("width"))/menuWidth*numColumn * new_width_column);
			}
		});
		$('#boss_menu_vertical ul.column').each(function(index, element) {
			if($(this).width() > currentWidth){
				$(this).width(parseFloat($(this).css("width"))/menuWidth*numColumn * new_width_column);
			}
		});
	}
	// end responsive
	hover();	
});

function hover(){
	var menu = jQuery("#boss_menu_vertical div.sub-inside");
	menuY = menu.offset().top;
	menuOuterH = menu.outerHeight();
	var list_li = jQuery("#boss_menu_vertical div.sub-inside ul.display-menu>li");
	
	list_li.each(function(idx) {
		
		var li_menuY = jQuery(this).offset().top;
		var dropdown = jQuery(this).find('div.dropdown');
		var dropdownOuterH = dropdown.outerHeight();
		
		if(menuOuterH <= dropdownOuterH || li_menuY - menuY <= dropdownOuterH){
			dropdown.css('top', menuY - li_menuY - 1 + 'px');
		}
		else{
			var temp = menuOuterH - (li_menuY - menuY);
			if(temp <= dropdownOuterH){
				var this_outerH = jQuery(this).outerHeight();
				dropdown.css('top', 0 - (dropdownOuterH - this_outerH) + 'px');
			}
		}
	});
}