/*-----------------------------------------------------------------------------------

	Template Name: Skinura - Skin Care HTML Template
	URI: pixelfit.agency
	Description: Skinura – Skincare & Beauty HTML Template is a modern, customizable, and fully responsive template designed for skincare clinics, beauty salons, dermatology centers, and cosmetic brands to showcase their services, treatments, products, and team with elegant layouts and engaging user experience.
	Author: Pixelfit
	Author URI: https://themeforest.net/user/pixelfit
	Version: 1.0.0

-----------------------------------------------------------------------------------

/***************************************************
==================== JS INDEX ======================
****************************************************
01. PreLoader Js
02. Nice Select Js
03. mobile menu Js
04. Sticky Header Js
05. offcanvas
06. Common Js
07. Smooth Scroll Js
08. Horizontal scroll
09. back-to-top
10. magnificPopup img view
11. Counter Js
12. Wow Js	
13. Quantity Number js
14. ScrollSmoother
****************************************************/

(function ($) {
   "use strict";

    var windowOn = $(window);

    // Main Menu

    let pfMainMenu = $('.pf-main-menu > nav, .pf-offcanvas-menu > nav');

    if($(pfMainMenu).find('.sub-menu').length != 0){
      $(pfMainMenu).find('.sub-menu').parent().append('<span class="dd-trigger"><i class="far fa-angle-down"></i></span>');
    }

    // Offcanvas
    $(".pf-header-toggle").on('click',function(){
        $(".pf-offcanvas").addClass("pf-offcanvas-active");
        $(".pf-offcanvas-overlay").addClass("overlay-active");
    });
    $(".pf-offcanvas-close-button, .pf-offcanvas-overlay").on('click',function(){
        $(".pf-offcanvas").removeClass("pf-offcanvas-active");
        $(".pf-offcanvas-overlay").removeClass("overlay-active");
    });

    // Offcanvas Mobile Menu
    let pfMenuHTML = $(".pf-mobile-menu-active > ul").clone();
    let pfOffcanvasMenu = $(".pf-offcanvas-menu > nav");
    pfOffcanvasMenu.append(pfMenuHTML);

    let pfSideMenuToggle = $('span.dd-trigger');

    $(pfSideMenuToggle).on('click',function(){
         $(this).siblings('.sub-menu').slideToggle();
         $(this).parent().toggleClass('active');
    });

    //===== Preloader
	windowOn.on('load', function() {
		$('.preloader').fadeOut(500);
	})

    // sticky js 
    windowOn.on('scroll', function () {
        var scroll = windowOn.scrollTop();
        if (scroll < 10) {
            $("#pf-header-sticky").removeClass("header-sticky");
        } else {
            $("#pf-header-sticky").addClass("header-sticky");
        }
    });

    // Back To Top
    var $backToTop = $(".back-to-top");
    $backToTop.hide();

    windowOn.on('scroll', function() {
        if ($(this).scrollTop() > 100) {
            $backToTop.fadeIn();
        } else {
            $backToTop.fadeOut();
        }
    });

    $backToTop.on('click', function(e) {
        $("html, body").animate({ scrollTop: 0 }, 500);
    });

      // faq class add remove
    $('.pf-accordion-button').on('click',function(){
      $(".pf-accordion-item").removeClass("active");
      $(this).closest('.pf-accordion-item').addClass('active');
    });

    // Team Section Js
    $('.pf-team-box').on('mouseenter', function () {
        $('.pf-team-box').removeClass('active');
        $(this).addClass('active');
    });

    // data bg img 
    $("[data-bg-img]").each(function () {
        $(this).css("background-image", "url(" + $(this).attr("data-bg-img") + ")")
    })

    // img popup
    $('.popup-img').magnificPopup({
        type: 'image'
      });

    // video popup
    $('.popup-video').magnificPopup({
        type: 'iframe'
      });
      

    //===== Nice select js
    if ($('select').length){
        $('select').niceSelect();
    }

	// Counter Js
	if (typeof PureCounter !== 'undefined') {
        new PureCounter();
    }

    //======= Quantity Number js

    $('.quantity-down').on('click', function(){
        var numProduct = Number($(this).next().val());
        if(numProduct > 1) $(this).next().val(numProduct - 1);
    });
    $('.quantity-up').on('click', function(){
        var numProduct = Number($(this).prev().val());
        $(this).prev().val(numProduct + 1);
    });


    // GSAP ScrollSmoother

    if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {

        gsap.registerPlugin(ScrollTrigger);

        if (typeof ScrollSmoother !== 'undefined') {
            ScrollSmoother.create({
                smooth: 1.35,
                effects: true,
                smoothTouch: 0.15,
            });
        }
    }

    // Services page with related services
    if (windowOn.width() > 991 && typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {

        const sectionSelector = ".pf-service-section";
        let pfTabTriggers = [];

        function initTabPins() {

            // Kill only our triggers (SAFE)
            pfTabTriggers.forEach(trigger => trigger.kill());
            pfTabTriggers = [];

            // Only visible tab cards
            $('.tab-pane.show.active .pf-services-tab-box').each(function () {

                let trigger = ScrollTrigger.create({
                    trigger: this,
                    start: "top 15%",
                    endTrigger: sectionSelector,
                    end: "bottom 80%",
                    pin: true,
                    pinSpacing: false,
                    scrub: true,
                    markers: false
                });

                pfTabTriggers.push(trigger);
            });
        }

        // Init on load
        windowOn.on('load', function () {
            initTabPins();
        });

        // Re-init on tab change
        $('button[data-bs-toggle="tab"]').on('shown.bs.tab', function () {
            setTimeout(function () {
                initTabPins();
                ScrollTrigger.refresh();
            }, 200);
        });

    }

    // Services Details Page 
        var width = windowOn.width();
        if (width > 768) { 
            "use strict";
            $(function () {
                let cards = gsap.utils.toArray(".pf-services-details-wrapper .pf-services-tab-box");
                let stickDistance = 300; 
                let lastCardST = ScrollTrigger.create({
                    trigger: cards[cards.length - 1],
                    start: "bottom bottom",
                    markers: false 
                });
                cards.forEach((card, index) => {
                    ScrollTrigger.create({
                        trigger: card,
                        start: "top 15%", 
                        end: () => lastCardST.start + stickDistance, 
                        pin: true,      
                        pinSpacing: false, 
                        ease: "none",    
                        scrub: true,     
                        toggleActions: "reverse none none reverse",
                        markers: false 
                    });
                });
            });
        }

    // Home One Services Section


        if (windowOn.width() > 991) {

            const section = document.querySelector(".pf-services-area");

            // Left pinned content
            gsap.utils.toArray(".pf-services-pin").forEach((pin) => {
                ScrollTrigger.create({
                    trigger: pin,
                    start: "top 30%",         
                    endTrigger: section,       
                    end: "bottom bottom",
                    pin: true,
                    pinSpacing: true,
                    scrub: true,
                    markers: false
                });
            });

            // Right stacked cards
            gsap.utils.toArray(".pf-services-right .pf-services-item").forEach((card) => {
                ScrollTrigger.create({
                    trigger: card,
                    start: "top 15%",
                    endTrigger: section,       
                    end: "bottom bottom",      
                    pin: true,
                    pinSpacing: false,
                    scrub: true,
                    markers: false
                });
            });

        }

        // Home Two Services horizontal scroll js
        	let horizontalSection = document.querySelector('.horizontal-scroll');
            if (horizontalSection) {
                gsap.to('.horizontal-scroll', {
                    x: () => horizontalSection.scrollWidth * -1,
                    xPercent: 100,
                    scrollTrigger: {
                        trigger: '.horizontal-scroll',
                        start: 'top 35%',
                        end: '+=2000px',
                        pin: '.pfservices-area',
                        scrub: 1.4,
                        invalidateOnRefresh: true
                    }
                });
            }

    //  Logo Slider
    var swiper_text = new Swiper(".pf-logo-slider-active", {
        slidesPerView: 'auto',
        spaceBetween: 120,
        freemode: true,
        centeredSlides: false,
        loop: true,
        speed: 5000,
        allowTouchMove: false,
          autoplay: {
          delay: 1,
          disableOnInteraction: true,
          },
      });
     
    // Testimonials Slider Style One
    var testimonialsSliderActive = new Swiper(".testimonials-slider-active", {
      slidesPerView: 4,
      spaceBetween: 20,
      freemode: true,
      centeredSlides: false,
      loop: true,
      speed: 10000,
      autoplay: {
          delay: 1,
          disableOnInteraction: true,
        },
        breakpoints: {
            // when window width is >= 640px
            300: {
            slidesPerView: 1,
            spaceBetween: 20
            },
            // when window width is >= 768px
            768: {
            slidesPerView: 2,
            spaceBetween: 30
            },
            // when window width is >= 1024px
            1200: {
            slidesPerView: 3,
            spaceBetween: 40
            },
            1400: {
            slidesPerView: 4,
            spaceBetween: 40
            }
        }
    });
    // Testimonials Slider Style Two
    var reviewSliderActive = new Swiper(".review-slider-active", {
      slidesPerView: 3,
      spaceBetween: 30,
      autoplay: true,
      loop: true,
      
      breakpoints: {
            // when window width is >= 640px
            300: {
            slidesPerView: 1,
            spaceBetween: 20
            },
            // when window width is >= 768px
            768: {
            slidesPerView: 2,
            spaceBetween: 30
            },
            // when window width is >= 1024px
            1200: {
            slidesPerView: 2,
            spaceBetween: 40
            },
            1400: {
            slidesPerView: 3,
            spaceBetween: 40
            }
        }
    });

    // // Three Number Testimonial Js Start
    // =========================================================================================
    function initTestimonialSlider() {
        $('.pf-testimonial').each(function () {
            var $section  = $(this);
            var $sliderEl = $section.find('.testimonials-slider-three-active');

            if (!$sliderEl.length) return;

            var pfTestimonial = new Swiper($sliderEl[0], {
                loop: true,
                speed: 600,
                navigation: {
                    nextEl: $section.find('.pf-testimonial-three-next')[0],
                    prevEl: $section.find('.pf-testimonial-three-prev')[0],
                },
                on: {
                    init: function () {
                        updateContent(this, $section);
                    },
                    slideChange: function () {
                        updateContent(this, $section);
                    }
                }
            });
        });
    }

    function updateContent(swiper, $section) {
        var activeSlide = swiper.slides[swiper.activeIndex];
        if (!activeSlide) return;

        var rate = parseFloat(activeSlide.getAttribute('data-rate')) || 0;
        var img  = activeSlide.getAttribute('data-img');

        // --- Smooth rate animation ---
        var $rateEl = $section.find('.pf-testimonial-rate-value');
        var current = parseFloat($rateEl.text()) || 0;

        if (current !== rate) {
            let start = current;
            let end = rate;
            let duration = 600; // in ms
            let startTime = null;

            function animateNumber(timestamp) {
                if (!startTime) startTime = timestamp;
                let progress = timestamp - startTime;
                let val = start + (end - start) * Math.min(progress / duration, 1);
                $rateEl.text(Math.round(val));
                if (progress < duration) {
                    requestAnimationFrame(animateNumber);
                }
            }
            requestAnimationFrame(animateNumber);
        }

        // --- Image fade ---
        if (img) {
            var $img = $section.find('.pf-testimonial-thumb img');
            if ($img.attr('src') === img) return;

            var preload = new Image();
            preload.src = img;

            preload.onload = function () {
                $img.addClass('is-changing');
                setTimeout(function () {
                    $img.attr('src', img);
                    $img.removeClass('is-changing');
                }, 150);
            };
        }
    }

    // Initialize slider on window load
    windowOn.on('load', function () {
        initTestimonialSlider();
    });
    // ===============================================================================
    // // Three Number Testimonial Js End
    
    // Testimonials Slider Style Four
    var testimonialsSliderFourActive = new Swiper(".testimonials-slider-four-active", {
      slidesPerView: 2,
      spaceBetween: 30,
      breakpoints: {
            // when window width is >= 640px
            300: {
            slidesPerView: 1,
            spaceBetween: 20
            },
            // when window width is >= 768px
            768: {
            slidesPerView: 2,
            spaceBetween: 30
            },
            // when window width is >= 992px
            992: {
            slidesPerView: 2,
            spaceBetween: 30
            },
            // when window width is >= 1024px
            1200: {
            slidesPerView: 2,
            spaceBetween: 40
            },
            
        }
    });
    // Slick Slider Product Single page slider
    if ($('.product-big-slider').length) {
        $('.product-big-slider').slick({
            dots: false,
            arrows: false,
            speed: 800,
            autoplay: true,
            fade: true,
            asNavFor: '.product-thumb-slider',
            slidesToShow: 1,
            slidesToScroll: 1,
            prevArrow: '<div class="prev"><i class="far fa-angle-left"></i></div>',
            nextArrow: '<div class="next"><i class="far fa-angle-right"></i></div>'
        });
    }

    if ($('.product-thumb-slider').length) {
        $('.product-thumb-slider').slick({
            dots: false,
            arrows: false,
            speed: 800,
            autoplay: true,
            asNavFor: '.product-big-slider',
            vertical: true,
            focusOnSelect: true,
            slidesToShow: 3,
            slidesToScroll: 1,
            prevArrow: '<div class="prev"><i class="far fa-angle-left"></i></div>',
            nextArrow: '<div class="next"><i class="far fa-angle-right"></i></div>'
        });
    }

    ////////////////////////////////////////////////////
	// pf. tp-postbox-thumb-slider-active
	var pfPostboxThumbSliderActive = new Swiper('.pf-postbox-thumb-slider-active', {
		slidesPerView: 1,
		loop: true,
		autoplay: false,
		arrow: false,
		spaceBetween: 0,
		speed: 1000,
		effect: 'fade',
		a11y: false,

		// Navigation arrows
		navigation: {
			prevEl: '.pf-postbox-arrow-prev',
			nextEl: '.pf-postbox-arrow-next',
		},

	});
    
    new WOW().init();


})(jQuery);

