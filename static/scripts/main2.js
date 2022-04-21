/*
	Forty by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
*/

(function($) {

	var	$window = $(window),
		$body = $('body'),
		$wrapper = $('#wrapper'),
		$header = $('#header'),
		$banner = $('#banner');


	// Breakpoints.
		breakpoints({
			xlarge:    ['1281px',   '1680px'   ],
			large:     ['981px',    '1280px'   ],
			medium:    ['737px',    '980px'    ],
			small:     ['481px',    '736px'    ],
			xsmall:    ['361px',    '480px'    ],
			xxsmall:   [null,       '360px'    ]
		});

	/**
	 * Applies parallax scrolling to an element's background image.
	 * @return {jQuery} jQuery object.
	 */
	$.fn._parallax = (browser.name == 'ie' || browser.name == 'edge' || browser.mobile) ? function() { return $(this) } : function(intensity) {

		var	$window = $(window),
			$this = $(this);

		if (this.length == 0 || intensity === 0)
			return $this;

		if (this.length > 1) {

			for (var i=0; i < this.length; i++)
				$(this[i])._parallax(intensity);

			return $this;

		}

		if (!intensity)
			intensity = 0.25;

		$this.each(function() {

			var $t = $(this),
				on, off;

			on = function() {

				$t.css('background-position', 'center 100%, center 100%, center 0px');

				$window
					.on('scroll._parallax', function() {

						var pos = parseInt($window.scrollTop()) - parseInt($t.position().top);

						$t.css('background-position', 'center ' + (pos * (-1 * intensity)) + 'px');

					});

			};

			off = function() {

				$t
					.css('background-position', '');

				$window
					.off('scroll._parallax');

			};

			breakpoints.on('<=medium', off);
			breakpoints.on('>medium', on);

		});

		$window
			.off('load._parallax resize._parallax')
			.on('load._parallax resize._parallax', function() {
				$window.trigger('scroll');
			});

		return $(this);

	};

	// Play initial animations on page load.
		$window.on('load', function() {
			window.setTimeout(function() {
				$body.removeClass('is-preload');
			}, 100);
		});

	// Clear transitioning state on unload/hide.
		$window.on('unload pagehide', function() {
			window.setTimeout(function() {
				$('.is-transitioning').removeClass('is-transitioning');
			}, 250);
		});

	// Fix: Enable IE-only tweaks.
		if (browser.name == 'ie' || browser.name == 'edge')
			$body.addClass('is-ie');

	// Scrolly.
		$('.scrolly').scrolly({
			offset: function() {
				return $header.height() - 2;
			}
		});

	// Tiles.
		var $tiles = $('.tiles > article');

		$tiles.each(function() {

			var $this = $(this),
				$image = $this.find('.image'), $img = $image.find('img'),
				$link = $this.find('.link'),
				x;

			// Image.

				// Set image.
					$this.css('background-image', 'url(' + $img.attr('src') + ')');

				// Set position.
					if (x = $img.data('position'))
						$image.css('background-position', x);

				// Hide original.
					$image.hide();

			// Link.
				if ($link.length > 0) {

					$x = $link.clone()
						.text('')
						.addClass('primary')
						.appendTo($this);

					$link = $link.add($x);

					$link.on('click', function(event) {

						var href = $link.attr('href');

						// Prevent default.
							event.stopPropagation();
							event.preventDefault();

						// Target blank?
							if ($link.attr('target') == '_blank') {

								// Open in new tab.
									window.open(href);

							}

						// Otherwise ...
							else {

								// Start transitioning.
									$this.addClass('is-transitioning');
									$wrapper.addClass('is-transitioning');

								// Redirect.
									window.setTimeout(function() {
										location.href = href;
									}, 500);

							}

					});

				}

		});

	// Header.
		if ($banner.length > 0
		&&	$header.hasClass('alt')) {

			$window.on('resize', function() {
				$window.trigger('scroll');
			});

			$window.on('load', function() {

				$banner.scrollex({
					bottom:		$header.height() + 10,
					terminate:	function() { $header.removeClass('alt'); },
					enter:		function() { $header.addClass('alt'); },
					leave:		function() { $header.removeClass('alt'); $header.addClass('reveal'); }
				});

				window.setTimeout(function() {
					$window.triggerHandler('scroll');
				}, 100);

			});

		}

	// Banner.
		$banner.each(function() {

			var $this = $(this),
				$image = $this.find('.image'), $img = $image.find('img');

			// Parallax.
				$this._parallax(0.275);

			// Image.
				if ($image.length > 0) {

					// Set image.
						$this.css('background-image', 'url(' + $img.attr('src') + ')');

					// Hide original.
						$image.hide();

				}

		});

	// Menu.
		var $menu = $('#menu'),
			$menuInner;

		$menu.wrapInner('<div class="inner"></div>');
		$menuInner = $menu.children('.inner');
		$menu._locked = false;

		$menu._lock = function() {

			if ($menu._locked)
				return false;

			$menu._locked = true;

			window.setTimeout(function() {
				$menu._locked = false;
			}, 350);

			return true;

		};

		$menu._show = function() {

			if ($menu._lock())
				$body.addClass('is-menu-visible');

		};

		$menu._hide = function() {

			if ($menu._lock())
				$body.removeClass('is-menu-visible');

		};

		$menu._toggle = function() {

			if ($menu._lock())
				$body.toggleClass('is-menu-visible');

		};

		$menuInner
			.on('click', function(event) {
				event.stopPropagation();
			})
			.on('click', 'a', function(event) {

				var href = $(this).attr('href');

				event.preventDefault();
				event.stopPropagation();

				// Hide.
					$menu._hide();

				// Redirect.
					window.setTimeout(function() {
						window.location.href = href;
					}, 250);

			});

		$menu
			.appendTo($body)
			.on('click', function(event) {

				event.stopPropagation();
				event.preventDefault();

				$body.removeClass('is-menu-visible');

			})
			.append('<a class="close" href="#menu">Close</a>');

		$body
			.on('click', 'a[href="#menu"]', function(event) {

				event.stopPropagation();
				event.preventDefault();

				// Toggle.
					$menu._toggle();

			})
			.on('click', function(event) {

				// Hide.
					$menu._hide();

			})
			.on('keydown', function(event) {

				// Hide on escape.
					if (event.keyCode == 27)
						$menu._hide();

			});

		
		
		

		// Menu.
		var $popupDetailsArray = $('.popup-details'),
			$popupDetailsInner;

		for(popupDetails of $popupDetailsArray){
			$popupDetails = $(popupDetails);

			 $popupDetails.wrapInner('<div class="inner"></div>');
		
			 $popupDetailsInner = $popupDetails.children('.inner');
			 $popupDetails._locked = false;
	 
			 
	 
			 $popupDetails._lock = function() {
	 
				 if ($popupDetails._locked)
					 return false;
	 
				 $popupDetails._locked = true;
	 
				 window.setTimeout(function() {
					 $popupDetails._locked = false;
				 }, 350);
	 
				 return true;
	 
			 };
	 
			 
	 
			 $popupDetails._show = function() {
	 
				 if ($popupDetails._lock())
					 $body.addClass('is-popup-details-visible');
	 
			 };
	 
			 $popupDetails._hide = function() {
	 
				 if ($popupDetails._lock())
					 $body.removeClass('is-popup-details-visible');
			 };
	 
			 $popupDetails._toggle = function() {
				 if ($popupDetails._lock())
					 $body.toggleClass('is-popup-details-visible');
	 
			 };
	 
			 $popupDetailsInner
				 .on('click', function(event) {
					 event.stopPropagation();
				 })
				 .on('click', 'a', function(event) {
	 
					 var href = $(this).attr('href');
	 
					 event.preventDefault();
					 event.stopPropagation();
	 
					 // Hide.
						 $popupDetails._hide();
	 
					 // Redirect.
						 window.setTimeout(function() {
							 window.location.href = href;
						 }, 250);
	 
				 });
	 
			 $popupDetails
				 .appendTo($body)
				 .on('click', function(event) {
					 event.stopPropagation();
					 event.preventDefault();
	 
					 $body.removeClass('is-popup-details-visible');
	 
				 })
				 .append('<a class="close" href="#popup-details">Close</a>');




		}
		
		

		


		

		// $body
		// 	.on('click', 'a[href="#popup-details"]', function(event) {
		// 		console.log("clicked2");
		// 		event.stopPropagation();
		// 		event.preventDefault();

		// 		// Toggle.
		// 			$popupDetails._toggle();

		// 	})
		// 	.on('click', function(event) {

		// 		// Hide.
		// 			$popupDetails._hide();

		// 	})
		// 	.on('keydown', function(event) {

		// 		// Hide on escape.
		// 			if (event.keyCode == 27)
		// 				$popupDetails._hide();

		// 	});

			var popupChart;

			$(document).on('click', '.driver', function(event) {
				// console.log($popupDetails);
				
				var obj = JSON.parse(event.currentTarget.id.replace(/\'/g, '"'));

				console.log(obj);


				$("#popup-name").text(obj.name);
				$("#popup-points").text(obj.points);
				$("#popup-price").text(obj.price);
				$("#popup-sr").text(obj.streak_race);
				$("#popup-sq").text(obj.streak_quali);
				$("#popup-image").attr('src', obj.imageUrl);
				$("#popup-wins").text(obj.wins);
				$("#popup-podiums").text(obj.podiums);
				$("#popup-poles").text(obj.poles);
				$("#popup-best-finish").text(obj.best_finish);
				$("#popup-best-finish-count").text(obj.best_finish_count);
				$("#popup-fastest-laps").text(obj.fastest_laps);
				$("#popup-place-of-birth").text(obj.place_of_birth);



				
				var labels = obj.price_change_data.map(function(e) {
					return e.game_period_id;
				});
				var data = obj.price_change_data.map(function(e) {
					return e.price;
				});

				var ctx = $('#popup-price-chart');

				Chart.defaults.global.legend.display = false;

				function graphColor (data){
					if (data[0] <= data[data.length-1]){
						return 'green';
					}
					else{
						return 'red';
					}
				}

				function graphColorRGBA (data){
					if (data[0] <= data[data.length-1]){
						return 'rgba(0,128,0,0.2)';
					}
					else{
						return 'rgba(255,0,0,0.2)';
					}
				}

				if (popupChart) {
					popupChart.destroy();
				  }

				popupChart = new Chart(ctx, {
					type: "line",
					data: {
						labels: labels,
						datasets: [{
						data: data,
						pointBackgroundColor: graphColor(data),
						borderColor: graphColor(data),
						backgroundColor: graphColorRGBA(data),
						fill: true,
						}],
					},
					
					options: {
						responsive: true,
						maintainAspectRatio: false,
						tooltips: {
							displayColors: true,
							callbacks: {
								title: function(tooltipItems, data) { 
									return '';
								}
							}
						},
						layout: {
							padding: {
								top:10,
								bottom:10,
								left: 10,
								right: 10
							}
						},
						scales: {
						
							xAxes: [{
								display:true,
								// gridLines: {
								// 	zeroLineColor: '#ffffff',
								// 	color: '#ffffff'
								// }
								scaleLabel: {
									display: true,
									labelString: '2022 Race Index',
									fontSize: 16,
									fontColor: '#1e2021',
									fontFamily: "Source Sans Pro",
									fontStyle: 'bold'
								  }
								
							}],

							yAxes: [{
								display:true,
								// gridLines: {
								// 	zeroLineColor: '#ffffff',
								// 	color: '#ffffff'
								// }
							}]
						}
					}
				});





				event.stopPropagation();
				event.preventDefault();

				// Toggle.
				$popupDetails._toggle();

			})
			.on('click', function(event) {

				// Hide.
				if (popupChart) {
					popupChart.destroy();
				  }
					$popupDetails._hide();

			})
			.on('keydown', function(event) {

				// Hide on escape.
				if (popupChart) {
					popupChart.destroy();
				  }
					if (event.keyCode == 27)
						$popupDetails._hide();

			});
		

		

		

		

})(jQuery);




