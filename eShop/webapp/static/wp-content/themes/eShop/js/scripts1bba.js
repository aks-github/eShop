/*-----------------------------------------------------------------------------------*/
/*	Toledo Custom Script
/*-----------------------------------------------------------------------------------*/

jQuery.noConflict();
jQuery(document).ready(function(){

	//menu		
	jQuery(".main_menu .menu").menu({modify_position:true});
	
	// improves menu for mobile devices
	jQuery('.main_menu ul:eq(0)').mobileMenu({
	  switchWidth: 765,                   							//width (in px to switch at)
	  topOptionText: jQuery('.main_menu').data('selectname'),     	//first option text
	  indentString: '&nbsp;&nbsp;&nbsp;'  							//string for indenting nested items
	});
	
	jQuery('.flexslider').flexslider();
	
	jQuery('.widget-quote blockquote').quovolver();

  jQuery('.portfolio-image a').hoverdir();

  jQuery('.gallery-image a').hoverdir();

  jQuery(document).ready(function(){
    jQuery("area[rel^='prettyPhoto']").prettyPhoto();

    jQuery("a[rel^='prettyPhoto']").prettyPhoto();
        
    jQuery(".gallery:first a[rel^='prettyPhoto']").prettyPhoto({animation_speed:'normal',theme:'light_square',slideshow:3000, autoplay_slideshow: true});
    jQuery(".gallery:gt(0) a[rel^='prettyPhoto']").prettyPhoto({animation_speed:'fast',slideshow:10000, hideflash: true});
    
  }); 
	
	//When page loads...
	jQuery(".tab_content").hide(); //Hide all content
	jQuery("ul.tabs li:first").addClass("active").show(); //Activate first tab
	jQuery(".tab_content:first").show(); //Show first tab content

	//On Click Event
	jQuery("ul.tabs li").click(function() {

		jQuery("ul.tabs li").removeClass("active"); //Remove any "active" class
		jQuery(this).addClass("active"); //Add "active" class to selected tab

		return false;
	});
	
	// setup ul.tabs to work as tabs for each div directly under div.panes
	jQuery("ul.tabs").tabs("div.panes > div");
	
	// scroll body to 0px on click
	jQuery(".backtop a").click(function () {
		jQuery("body,html").animate({
			scrollTop: 0
		}, 800);
		return false;
	});



	// Portfolio filter
  // actiavte portfolio sorting
  elem = jQuery("#portfolio-sort-container");
  if (elem.is (".portfolio-sort-container")) {
    jQuery.extend( jQuery.Isotope.prototype, {
      _customModeReset : function() { 
      
        this.fitRows = {
            x : 0,
            y : 0,
            height : 0
          };
      
       },
      _customModeLayout : function( $elems ) { 
      
        var instance    = this,
            containerWidth  = this.element.width(),
            props       = this.fitRows,
            margin      = (containerWidth / 100) * 2, //margin based on %
            extraRange    = 2; // adds a little range for % based calculation error in some browsers
      
          $elems.css({visibility:'visible'}).each( function() {
            var $this = jQuery(this),
                atomW = $this.outerWidth(),
                atomH = $this.outerHeight(true);
            
            if ( props.x !== 0 && atomW + props.x > containerWidth + extraRange ) {
              // if this element cannot fit in the current row
              props.x = 0;
              props.y = props.height;
            } 
          
          //webkit gets blurry elements if position is a float value
          props.x = Math.round(props.x);
          props.y = Math.round(props.y);
         
            // position the atom
            instance._pushPosition( $this, props.x, props.y );
          
            props.height = Math.max( props.y + atomH, props.height );
            props.x += atomW + margin;
        
        jQuery('#portfolio-sort-container').css({visibility:"visible", opacity:1});
        jQuery('#filters').css({visibility:"visible", opacity:1});
        
        
          });
      
      },
      _customModeGetContainerSize : function() { 
      
        return { height : this.fitRows.height };
      
      },
      _customModeResizeChanged : function() { 
      
        return true;
        
       }
    });
    
      var $container = jQuery('#portfolio-sort-container').css({visibility:"visible", opacity:0});

        $container.isotope({
          itemSelector : '.isotope-item',
      layoutMode : 'customMode'
        });
        
        
        var $optionSets = jQuery('#portfolio .sort_by_cat'),
            $optionLinks = $optionSets.find('a');

        $optionLinks.click(function(){
          var $this = jQuery(this);
          // don't proceed if already selected
          if ( $this.hasClass('active_sort') ) {
            return false;
          }
          var $optionSet = $this.parents('.sort_by_cat');
          $optionSet.find('.active_sort').removeClass('active_sort');
          $this.addClass('active_sort');
    
          // make option object dynamically, i.e. { filter: '.my-filter-class' }
          var options = {},
              key = $optionSet.attr('data-option-key'),
              value = $this.attr('data-option-value');
          // parse 'false' as false boolean
          value = value === 'false' ? false : value;
          options[ key ] = value;
          if ( key === 'layoutMode' && typeof changeLayoutMode === 'function' ) {
            // changes in layout modes need extra logic
            changeLayoutMode( $this, options )
          } else {
            // otherwise, apply new options
            $container.isotope( options );
          }
          
          return false;
      });
  };
	
	// Blog Isotop Masonry Layout
	// actiavte blog masonry isotope right sidebar page layout
	elem = jQuery("#template-blog-masonry");
	if (elem.is (".template-blog-masonry")) {	

	    var $container = jQuery('#container-blog-two-col')
		// initialize Isotope
		$container.isotope({
			// options...
			resizable: true, //
			// set columnWidth to a percentage of container width
			masonry: { }
	    });
		
		jQuery(window).bind("resize", resizeWindow);
        function resizeWindow( e ) {
            var newWindowWidth = jQuery(window).width();

            jQuery('#container-blog-two-col').isotope( 'reLayout' )
        }
		
	};
	
	// actiavte blog masonry isotope full page layout
	elem = jQuery("#template-blog-masonry");
	if (elem.is (".template-blog-masonry")) {	

	    var $container = jQuery('#container-blog-full')
		// initialize Isotope
		$container.isotope({
			// options...
			resizable: true, //
			// set columnWidth to a percentage of container width
			masonry: { }
	    });
		
		jQuery(window).bind("resize", resizeWindow);
        function resizeWindow( e ) {
            var newWindowWidth = jQuery(window).width();

            jQuery('#container-blog-full').isotope( 'reLayout' )
        }
		
	};

	//Toggle
	jQuery(".togglebox").hide();
	//slide up and down when click over heading 2
	
	jQuery("h4").click(function(){
	// slide toggle effect set to slow you can set it to fast too.
	jQuery(this).toggleClass("active").next(".togglebox").slideToggle("slow");
	
	return true;
	
	});

	jQuery(function() {
      // setup ul.tabs to work as tabs for each div directly under div.panes
      jQuery("ul.tabs").tabs("div.panes > div");
  });


  jQuery(function() {
      // setup ul.tabs to work as tabs for each div directly under div.panes
      jQuery("ul.tabs").tabs("div.panes > div");


    jQuery("#tabs").tabs("div.panel");

    /* Tabs */
    jQuery('#tabs .panel:not(#tabs .panel)').hide();
    jQuery('#tabs li a').click(function(){
      var href = jQuery(this).attr('href');
      jQuery('#tabs li').removeClass('active');
      jQuery('div.panel').hide();
      jQuery('div' + href).show();
      jQuery(this).parent().addClass('active');
      jQuery.cookie('current_tab', href);
      return false;
    });
    if (jQuery('#tabs li.active').size()==0) {
      jQuery('#tabs li:first a').click();
    } else {
      jQuery('#tabs li.active a').click();
    }

    jQuery(".woocommerce_tabs").tabs("div.panel");

    /* Tabs */
    jQuery('.woocommerce_tabs .panel:not(.woocommerce_tabs .panel)').hide();
    jQuery('.woocommerce_tabs li a').click(function(){
      var href = jQuery(this).attr('href');
      jQuery('.woocommerce_tabs li').removeClass('active');
      jQuery('div.panel').hide();
      jQuery('div' + href).show();
      jQuery(this).parent().addClass('active');
      jQuery.cookie('current_tab', href);
      return false;
    });
    if (jQuery('.woocommerce_tabs li.active').size()==0) {
      jQuery('.woocommerce_tabs li:first a').click();
    } else {
      jQuery('.woocommerce_tabs li.active a').click();
    }
    
  });


	// Image Preloader
	/*jQuery(function() {
		jQuery('.portfolio-image img').hide();
		jQuery('.portfolio-image img').parent().parent().addClass('image-preloading');
	});

	jQuery(window).bind('load', function() {
		var i = 1;
		var imgs = jQuery('img').length;
		var int = setInterval(function() { 
			//console.log(i); check to make sure interval properly stops
			if(i >= imgs) clearInterval(int);
			jQuery('img:hidden').eq(0).fadeIn(500, function(){
				jQuery('.portfolio-image img').parent().parent().removeClass('image-preloading');
			});
			i++;
		});	
	});
	*/
	
});

/*-----------------------------------------------------------------------------------*/
/*	Image Hover
/*-----------------------------------------------------------------------------------*/

jQuery(function() {
	
	jQuery(".partners img").css("opacity","0.5");
	jQuery(".partners img").hover(function () {
	jQuery(this).stop().animate({ opacity: 1.0 }, "fast");  },
	function () {
	jQuery(this).stop().animate({ opacity: 0.5 }, "fast");  
	});
	
	jQuery(".more a").css("left","-10px");
	jQuery(".more a").hover(function () {
	jQuery(this).stop().animate({ left: "0px" }, "fast");  },
	function () {
	jQuery(this).stop().animate({ left: "-10px" }, "fast");  
	});
	
	jQuery(".widget .links li a").css("left","0");
	jQuery(".widget .links li a").hover(function () {
	jQuery(this).stop().animate({ left: "5px" }, "fast");  },
	function () {
	jQuery(this).stop().animate({ left: "0" }, "fast");  
	});

  jQuery(".project-title").fadeOut('fast');


  jQuery("#portfolio .isotope-item").mouseenter(function () {

    jQuery(this).find(".project-title").stop(true, true).fadeIn('normal');

     jQuery(".project-title").mouseleave(function () {
        jQuery(this).fadeOut('slow');
      });      

  });

});

/*-----------------------------------------------------------------------------------*/
/* Menu
/*-----------------------------------------------------------------------------------*/

jQuery.fn.menu = function(variables) 
{
	var defaults = 
	{
		modify_position:true,
		delay:300
	};
		
	var options = jQuery.extend(defaults, variables);
		
	return this.each(function()
	{
			
		var menu = jQuery(this),
			menuItems = menu.find(">li"),
			dropdownItems = menuItems.find(">ul").parent(),
			parentContainerWidth = menu.parent().width(),
			delayCheck = {};
			
		dropdownItems.find('li').andSelf().each(function()
		{	
			var currentItem = jQuery(this),
				sublist = currentItem.find('ul:first'),
        menuItemThis = currentItem.find('a:first'),
				showList = false;
				
			if(sublist.length) 
			{ 
        
				sublist.css({display:'block', opacity:0, visibility:'hidden'}); 
				var currentLink = currentItem.find('>a');
					
				currentLink.bind('mouseenter', function()
				{
          menuItemThis.removeClass("menu-button-change-back");
          menuItemThis.addClass("menu-button-change"); 
					sublist.stop().css({visibility:'visible'}).animate({opacity:1});
				});
					
				currentItem.bind('mouseleave', function()
				{
          menuItemThis.removeClass("menu-button-change");
          menuItemThis.addClass("menu-button-change-back");
					sublist.stop().animate({opacity:0}, function()
					{
						sublist.css({visibility:'hidden'});
					});
				});

			}
		
		});
			
	});
};


(function($){

  //variable for storing the menu count when no ID is present
  var menuCount = 0;
  
  //plugin code
  $.fn.mobileMenu = function(options){
    
    //plugin's default options
    var settings = {
      switchWidth: 768,
      topOptionText: 'Navigate to...',
      indentString: '&nbsp;&nbsp;&nbsp;'
    };
    
    
    //function to check if selector matches a list
    function isList($this){
      return $this.is('ul, ol');
    }
  
  
    //function to decide if mobile or not
    function isMobile(){
      return ($(window).width() < settings.switchWidth);
    }
    
    
    //check if dropdown exists for the current element
    function menuExists($this){
      
      //if the list has an ID, use it to give the menu an ID
      if($this.attr('id')){
        return ($('#mobileMenu-'+$this.attr('id')).length > 0);
      } 
      
      //otherwise, give the list and select elements a generated ID
      else {
        menuCount++;
        $this.attr('id', 'mobile-menu-'+menuCount);
        return ($('#mobileMenu-mobile-menu-'+menuCount).length > 0);
      }
    }
    
    
    //change page on mobile menu selection
    function goToPage($this){
      if($this.val() !== null){document.location.href = $this.val()}
    }
    
    
    //show the mobile menu
    function showMenu($this){
      $this.css('display', 'none');
      $('#mobileMenu-'+$this.attr('id')).show();
    }
    
    
    //hide the mobile menu
    function hideMenu($this){
      $this.css('display', '');
      $('#mobileMenu-'+$this.attr('id')).hide();
    }
    
    
    //create the mobile menu
    function createMenu($this){
      if(isList($this)){
                
        //generate select element as a string to append via jQuery
        var selectString = '<select id="mobileMenu-'+$this.attr('id')+'" class="mobileMenu">';
        
        //create first option (no value)
        selectString += '<option value="">'+settings.topOptionText+'</option>';
        
        //loop through list items
        $this.find('li').each(function(){
          
          //when sub-item, indent
          var levelStr = '';
          var len = $(this).parents('ul, ol').length;
          for(i=1;i<len;i++){levelStr += settings.indentString;}
          
          //get url and text for option
          var link = $(this).find('a:first-child').attr('href');
          var text = levelStr + $(this).clone().children('ul, ol').remove().end().text();
          
          //add option
          selectString += '<option value="'+link+'">'+text+'</option>';
        });
        
        selectString += '</select>';
        
        //append select element to ul/ol's container
        $this.parent().append(selectString);
        
        //add change event handler for mobile menu
        $('#mobileMenu-'+$this.attr('id')).change(function(){
          goToPage($(this));
        });
        
        //hide current menu, show mobile menu
        showMenu($this);
      } else {
        alert('mobileMenu will only work with UL or OL elements!');
      }
    }
    
    
    //plugin functionality
    function run($this){
      
      //menu doesn't exist
      if(isMobile() && !menuExists($this)){
        createMenu($this);
      }
      
      //menu already exists
      else if(isMobile() && menuExists($this)){
        showMenu($this);
      }
      
      //not mobile browser
      else if(!isMobile() && menuExists($this)){
        hideMenu($this);
      }

    }
    
    //run plugin on each matched ul/ol
    //maintain chainability by returning "this"
    return this.each(function() {
      
      //override the default settings if user provides some
      if(options){$.extend(settings, options);}
      
      //cache "this"
      var $this = $(this);
    
      //bind event to browser resize
      $(window).resize(function(){run($this);});

      //run plugin
      run($this);

    });
    
  };
  
})(jQuery);