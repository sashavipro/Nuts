// 1. ИМПОРТИРУЕМ СТИЛИ (Vite сам вытащит их в отдельный CSS-файл)
import '../sass/main.sass';
// 2. ИМПОРТИРУЕМ JQUERY И ДЕЛАЕМ ЕГО ГЛОБАЛЬНЫМ
// import '../libs/jquery/dist/jquery.min.js';
// window.$ = window.jQuery;
// if (typeof globalThis !== 'undefined') {
//     globalThis.$ = globalThis.jQuery = window.jQuery;
// }
import './jquery-global.js';

// 3. ИМПОРТИРУЕМ ВСЕ ПЛАГИНЫ
import '../libs/jquery/dist/jquery-ui-1.10.4.custom.min.js';
import '../libs/count/jquery.countTo.js';
import '../libs/swiper/dist/js/swiper.min.js';
import '../libs/gallery/simple-lightbox.min.js';
import '../libs/parallax/scrollax.min.js';
import '../libs/picturefill/picturefill.min.js';
import '../libs/sticky-sidebar/stickyfill.min.js';
import '../libs/scroll/jquery.mCustomScrollbar.js';
import '../libs/table/jquery.basictable.min.js';
import '../libs/tooltip/dist/js/tooltipster.bundle.min.js';
import '../libs/select2/dist/js/select2.min.js';

// jQuery(function($){

// 	});

// window.onload = function () {

// }

// инициализируем параллакс
jQuery(document).ready(function($){
  'use strict';
  $.Scrollax();
});

// функция гугл карты
// window.initMap = function() {
// 	var odessa = {lat: 46.484600, lng: 30.732600};
// 	var map = new google.maps.Map(document.getElementById('map'), {
// 		zoom: 15,
// 		center: odessa,
// 		styles: [
// 			{
// 					"featureType": "road",
// 					"elementType": "geometry",
// 					"stylers": [
// 							{
// 									"lightness": 100
// 							},
// 							{
// 									"visibility": "simplified"
// 							}
// 					]
// 			},
// 			{
// 					"featureType": "water",
// 					"elementType": "geometry",
// 					"stylers": [
// 							{
// 									"visibility": "on"
// 							},
// 							{
// 									"color": "#C6E2FF"
// 							}
// 					]
// 			},
// 			{
// 					"featureType": "poi",
// 					"elementType": "geometry.fill",
// 					"stylers": [
// 							{
// 									"color": "#C5E3BF"
// 							}
// 					]
// 			},
// 			{
// 					"featureType": "road",
// 					"elementType": "geometry.fill",
// 					"stylers": [
// 							{
// 									"color": "#D1D1B8"
// 							}
// 					]
// 			}
// 	]
//
// 	});
// 	var marker = new google.maps.Marker({
// 		position: odessa,
// 		map: map,
// 		icon: 'img/marker.svg'
// 	});
// }

(function ($) {

	// :: PreventDefault a Click
	$("a[href='#']").on('click', function (e) {
		e.preventDefault();
	});

	// создаем пустой блок под мобильное меню
	$('.top-header').before('<div class="mobile-menu d-lg-none"><div class="row"><div class="col-12"><div class="mobile-logo-wrap"></div><i class="nut-icon icons-close-button"></div></div></div>');
	// клонируем динамический логотип из десктопной версии в мобильную
	$('.top-header__logo .logo').clone().appendTo('.mobile-logo-wrap');

	// клонируем меню
	$('.menu_top').clone().appendTo('.mobile-menu');

	// показать/скрыть меню
  $('.mobile-menu-button, .mobile-menu .icons-close-button').click(function() {
		$('.mobile-menu').stop().slideToggle();
		$('.top-header').toggleClass('d-none');
	});

	// наполняем блок с меню другими элементами
	$('.logo_tel_mobile').insertBefore('.lang-menu');
	$('.logo_button_mobile').insertBefore('.lang-menu');
  $('.line_social').clone().appendTo('.mobile-line');
  $('.log_in').clone().appendTo('.mobile-line');
	$('.mobile-line ul.log_in').removeClass('d-none');

	// переносим навигацию слайдера
	$('.news-container .swiper-button-next').insertBefore('.news .wrap .navigation');
	$('.news-container .swiper-button-prev').insertBefore('.news .wrap .navigation');

	// модальное окно на плашке товара cо слайдером
	// $('.products-container .swiper-slide a').simpleLightbox();

	// инициализация таймера при скролле к блоку
	var blockScrolled = $('.timer');


	$(window).on('scroll', function () {

		if ( $(window).scrollTop() > blockScrolled.offset().top - $(window).height() / 2 ) {
			$('.timer__single').countTo();
			$(window).off('scroll');

		}

	});
	// $('.timer__single').countTo();

	// tabs

	$('ul.tabs__caption').on('click', 'li:not(.active)', function() {
    $(this)
      .addClass('active').siblings().removeClass('active')
      .closest('div.tabs').find('div.tabs__content').removeClass('active').eq($(this).index()).addClass('active');
	});

		//В зависимости от выбранной радио кнопки показ блока

		$(document).ready(function(){

			$('.radio__wrap input[type="radio"]').click(function(){

					var inputValue = $(this).attr("value");

					var targetBox = $("." + inputValue);

					$(".box").not(targetBox).hide();

					$(targetBox).show();

			});

	});

	$(document).ready(function(){

		$('.radio__wrapper_click input[type="radio"]').click(function(){

				var inputValue = $(this).attr("value");

				var targetBox = $("." + inputValue);

				$(".box").not(targetBox).hide();

				$(targetBox).show();


		});

		$('.radio__wrapper_click .radio-custom_last').click(function(){

			$(".box").css('display', 'none');

	});

});

	// tooltip

	$('.tooltip').tooltipster({
		animation: 'fade',
		delay: 200,
		// trigger: 'click',
		maxWidth: 106
 });

	// tables responsive
	$('#table').basictable();

	$('#table-breakpoint').basictable({
		breakpoint: 768
	});

	$('#table-container-breakpoint').basictable({
		containerBreakpoint: 485
	});

	$('#table-swap-axis').basictable({
		swapAxis: true
	});

	$('#table-force-off').basictable({
		forceResponsive: false
	});

	$('#table-no-resize').basictable({
		noResize: true
	});

	$('#table-two-axis').basictable();

	$('#table-max-height').basictable({
		tableWrapper: true
	});

	// окно корзины

	$('.logo_number').click(function() {
		$('.popup__cart').stop().slideToggle('swing');
	});

	$(document).mouseup(function (e){ // событие клика по веб-документу
		var div = $(".popup__cart"); // тут указываем класс элемента
		if (!div.is(e.target) // если клик был не по нашему блоку
		    && div.has(e.target).length === 0) { // и не по его дочерним элементам
			div.slideUp(); // скрываем его
		}
	});


	// if ($(window).width() <= '992'){
	// 	$('.popup__cart').clone().appendTo('.top-header');
	// }

	// fixed sidebar
	var elements = $('.sticky');
Stickyfill.add(elements);
	// $('#sidebar').stickySidebar({
	// 	containerSelector: '#main-content',
	// 	// innerWrapperSelector: '.sidebar__inner',
	// 	topSpacing: 20,
	// 	bottomSpacing: 20
	// });

	// Выпадающий список выбора языков (БЕЗОПАСНЫЙ КОД)
	var menuElem = document.getElementById('lang-menu');
	if (menuElem) {
		var titleElem = menuElem.querySelector('.title');
		document.addEventListener('click', function(event) {
			var target = event.target;
			var elem = event.target;

			while (target && target !== document) {
				if (target === menuElem) {
					if(elem.tagName === 'A') {
						titleElem.innerHTML = elem.textContent;
                        // Если есть иконки стран
                        if (getComputedStyle(elem, null)['backgroundImage'] !== 'none') {
                            titleElem.style.backgroundImage = getComputedStyle(elem, null)['backgroundImage'];
                        }
					}
					menuElem.classList.toggle('open');
					return;
				}
				target = target.parentNode;
			}
			menuElem.classList.remove('open');
		});
	}

	// $(document).ready(function(){

	// $('.header').before('<div class="mobile-menu d-lg-none">');
	// $('.menu').clone().appendTo('.mobile-menu');
	// $('.convizit-hamburger-box').click(function() {
	// 	$('.mobile-menu').stop().slideToggle();
	// });

	// });


	//initialize swiper when document ready
	var swiper = new Swiper('.news-container', {
		slidesPerView: 3,
		spaceBetween: 30,
		loop: true,
		// pagination: {
		//   el: '.swiper-pagination',
		//   type: 'fraction',
		// },
		navigation: {
			nextEl: '.swiper-button-next',
			prevEl: '.swiper-button-prev',
		},
		autoplay: {
			delay: 2500,
			disableOnInteraction: false,
		},
		breakpoints: {
			1024: {
				slidesPerView: 3,
				spaceBetween: 30,
			},
			920: {
				slidesPerView: 2,
				spaceBetween: 30,
			},
			578: {
				slidesPerView: 1,
				spaceBetween: 10,
			}
		}
	});

	$(".swiper-container").hover(function() {
    (this).swiper.autoplay.stop();
}, function() {
    (this).swiper.autoplay.start();
});

	//initialize swiper when document ready
	var swiper = new Swiper('.manufacturer-container', {
		slidesPerView: 1,
		spaceBetween: 30,
		loop: true,
		speed: 400,
		// pagination: {
		//   el: '.swiper-pagination',
		//   type: 'fraction',
		// },
		navigation: {
			nextEl: '.swiper-button-next',
			prevEl: '.swiper-button-prev',
		},
		autoplay: {
			delay: 2500,
			disableOnInteraction: false,
		},
		breakpoints: {
			1024: {
				slidesPerView: 1,
				spaceBetween: 30,
			},
			920: {
				slidesPerView: 1,
				spaceBetween: 30,
			},
			578: {
				slidesPerView: 1,
				spaceBetween: 10,
			}
		}
	});


	//initialize swiper when document ready
	var swiper = new Swiper('.products-container', {
		slidesPerView: 1,
		spaceBetween: 30,
		loop: true,
		speed: 400,
		// pagination: {
		//   el: '.swiper-pagination',
		//   type: 'fraction',
		// },
		navigation: {
			nextEl: '.swiper-button-next',
			prevEl: '.swiper-button-prev',
		},
		autoplay: 10000000,
		zoom: true,
		// autoplayDisableOnInteraction: false,
		// noSwiping: true,
		noSwiping: false,
		breakpoints: {
			1024: {
				slidesPerView: 1,
				spaceBetween: 30,
			},
			920: {
				slidesPerView: 1,
				spaceBetween: 30,
			},
			578: {
				slidesPerView: 1,
				spaceBetween: 10,
			}
		}
	});

	// задаем класс и data по дукументации плагина скролла

	$('.manufacturer .wrapper').addClass('mCustomScrollbar').attr('data-mcs-theme', 'dark');
	$(".manufacturer .wrapper").mCustomScrollbar({
		theme:"dark"
	});

	})(jQuery);
