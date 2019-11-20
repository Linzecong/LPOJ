(function ($) {
    "use strict";

    /*----------------------------
       		preloader active
       	------------------------------*/

    $(window).on('load', function () {
        jQuery(".preloader").fadeOut(500);
    });

    /*----------------------------
       		sticky Header
       	------------------------------*/

    $(window).on('scroll', function () {
        var scroll = $(window).scrollTop();
        if (scroll < 2) {
            $(".header-area").removeClass("sticky");
        } else {
            $(".header-area").addClass("sticky");
        }
    });

    /*----------------------------
       		main menu Active
       	------------------------------*/

    jQuery('#mobile-menu').meanmenu({
        meanMenuContainer: '.mobile-menu',
        meanScreenWidth: "991"
    });

    /*----------------------------
       		search form Active
       	------------------------------*/

    $('#close-btn').on('click', function () {
        $('#search-overlay').fadeOut();
        $('#search-btn').show();
    });
    $('#search-btn').on('click', function () {
        $('#search-overlay').fadeIn();
    });

    /*----------------------------
    		Counter Active
    	------------------------------*/

    $('.counter').counterUp({
        delay: 2,
        time: 1000
    });

    /*----------------------------
    		popup active
    	------------------------------*/

    $(".popup-video").magnificPopup({
        type: "iframe"
    });

    /*--------------------------
     Screenshot slider active
    ---------------------------- */
    $('.appnox-screenshot-slider').owlCarousel({
        autoplay: true,
        loop: true,
        dots: true,
        nav: false,
        responsive: {
            0: {
                items: 1
            },
            361: {
                items: 2
            },
            576: {
                items: 2
            },
            768: {
                items: 3
            },
            1000: {
                items: 4
            }
        }
    });

    /*----------------------------
        		testimonial slider Active
        	------------------------------*/

    $(".testimonial-wraper").owlCarousel({
        loop: true,
        autoplay: true,
        animateIn: 'zoomInDown',
        smartSpeed: 1000,
        dots: false,
        nav: true,
        navText: ["<i class='fa fa-long-arrow-left'></i>", "<i class='fa fa-long-arrow-right'></i>"],
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 1
            },
            1000: {
                items: 1
            }
        }
    });

    /*----------------------------
    		Client Slider Active
    	------------------------------*/

    $(".all-client-slider").owlCarousel({
        loop: true,
        autoplay: false,
        smartSpeed: 1000,
        dots: false,
        nav: false,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 2
            },
            1000: {
                items: 4
            }
        }
    });

    /*----------------------------
         		scrolltop active
         	------------------------------*/

    $('body').materialScrollTop();

    /*----------------------------
        		WOW active
        	------------------------------*/

    new WOW().init();

})(jQuery);