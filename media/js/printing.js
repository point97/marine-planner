(function () {
	function printModel (map, viewModel) {
		var self = this;
		self.$popover = $('#printing-popover');
		// show print dialog
		self.showPrintDialog = function (vm, event) {
            var width = $("#map-panel").width() + $("#legend:visible").width();

            self.$button = $(event.target).closest('.btn');

            // adjust the width depending on legend visibility
            if ($("#legend").is(":visible")) {
                width = width + 60;
            } else {
                width = width + 40;
            }

            self.isGoogle(/Google/.test(app.map.baseLayer.name));

            // set some default options
            self.shotHeight($(document).height());
            self.shotWidth(width);
            self.mapHeight($(document).height());

            self.mapWidth(width);
            self.thumbnail(false);
            self.showLegend(app.viewModel.showLegend() || false);
            self.ratio = self.shotHeight() / self.shotWidth();

            if (self.$popover.is(":visible")) {
                self.$popover.hide();
            } else {
                // hide the popover if already visible
                self.jobStatus("Waiting for PDF generation to complete.\nThis may take 30 - 60 seconds, depending on the complexity of the map.\n");
                self.showSpinner(true);
                self.thumbnail(false);
                self.$popover.show().draggable().position({
                    "my": "right top",
                    "at": "left middle",
                    "of": self.$button,
                    offset: "-200px"
                });
            }
		};

		// print server is enabled, don't show button without it
		self.enabled = ko.observable(true);

		self.jobStatus = ko.observable();
		self.showSpinner = ko.observable();

		// job options
		self.format = ko.observable("pdf");
		self.paperSize = ko.observable("letter");
		self.orientation = ko.observable("landscape");

		// final dimensions of image in pixels
		self.shotHeight = ko.observable();
		self.shotWidth = ko.observable();

		// read or write shot height/width in pixels or inches
	

		// dpi settings for phantomjs
		self.dpiWidth = 101.981;
        self.dpiHeight = 110.007;

		// working dimensions of map for rendering purposes
		self.mapHeight = ko.observable();
		self.mapWidth = ko.observable();

		// output options
		self.showLegend = ko.observable();
		self.borderLess = ko.observable(false);
		self.title = ko.observable();

		// job results
		self.download = ko.observable();
		self.thumbnail = ko.observable(false);

		// warn if baselayer is google
		self.isGoogle = ko.observable(false);
		self.units = ko.observable("pixels");

        self.token = 0;

		self.shotHeightDisplay = ko.computed({
			read: function () {
				var value = self.shotHeight();

				if (self.units() === 'inches') {
					value = value / self.dpiHeight;
				} else {
					value = parseInt(value, 10);
				}
				return value;
			},
			write: function (value) {
				if (self.units() === 'inches') {
					value = value * self.dpiHeight;
				}
				self.shotHeight(value);
			}
		});
		self.shotWidthDisplay = ko.computed({
			read: function () {		
				var value = self.shotWidth();

				if (self.units() === 'inches') {
					value = value / self.dpiWidth;
				} else {
					value = parseInt(value, 10);
				}
				return value;
			},
			write: function (value) {
				if (self.units() === 'inches') {
					value = value * self.dpiWidth;
				}
				self.shotWidth(value);
			}
		});

		// legend checkbox shows/hides real legend
		// update positon of popover
		self.showLegend.subscribe(function (newValue) {
			app.viewModel.showLegend(newValue);
		});

		self.units.subscribe(function (units) {
			var steps = units === 'inches' ? 0.1 : 1;
			// save the old value and adjust the steps
			$('.ui-spinner-input').each(function (i, input) {
				var $input = $(input), val = $input.val();
				// console.log(val);
				$input.spinner('option', { 'step': steps});
				$input.val(val);
			});
		});
		
		// lock aspect ratio with these subscriptions
		self.shotHeight.subscribe(function (newVal) {
			var width = newVal / self.ratio;
			if ($.isNumeric(width) && width !== self.shotWidth()) {
				self.shotWidth(width);		
			}
		});
		self.shotWidth.subscribe(function (newVal) {
			var height = newVal * self.ratio;
			if ($.isNumeric(height) && height !== self.shotHeight()) {
				self.shotHeight(height);		
			}
		});
		
		// borderless turned on will disable title and legend
		self.borderLess.subscribe(function (newVal) {
			if (newVal === true) {
				self.showLegend(false);
				self.oldTitle = self.title();
				self.title(null);
			} else {
				if (self.oldTitle) {
					self.title(self.oldTitle);
				}
			}
		});

        self.doPrint = function() {
            self.$popover.hide();
            self.token = (new Date()).getTime();

            document.forms['printDownloadForm']['token'].value = self.token;
            if (self.interval) {
                window.clearInterval(self.interval);
            }
            self.interval = setInterval(function() {
                function getCookie(name) {
                    // nonsense from https://developer.mozilla.org/en-US/docs/Web/API/document/cookie?redirectlocale=en-US&redirectslug=DOM%2Fdocument.cookie
                    return decodeURIComponent(document.cookie.replace(new RegExp("(?:(?:^|.*;)\\s*" + encodeURIComponent(name).replace(/[\-\.\+\*]/g, "\\$&") + "\\s*\\=\\s*([^;]*).*$)|^.*$"), "$1")) || null;
                }
                function tossCookie(name) {
                    document.cookie = encodeURIComponent(name) +
                                      "=deleted; expires=" +
                                      (new Date(0)).toUTCString();
                }

                var token = getCookie('token');
                if (token == self.token) {
                    tossCookie('token');
                    window.clearInterval(self.interval);
                    $('#print-modal').modal('hide');
                }
            }, 1000);
            $("#print-modal").modal('show');
            return true;
        }

		// print button in result dialog
		self.print = function () {

			var w = window.open(self.download());
			setTimeout(function () {
				w.print();
				w.close();
			}, 500);
				
		};

		self.downloadFile = function (self,event) {
			var $modal = $(event.target).closest('.modal');
			$modal.modal('hide');
			window.open(self.download());
		};

		// handle export button in print popover
		self.sendJob = function (self, event) {
			var mapHeight, mapWidth;
			event.preventDefault();
			self.$popover.hide();
			$("#print-modal").modal('show');

			if (self.borderLess()) {
				mapHeight = $('#map-panel').height() - 2;
				mapWidth = $("#map-panel").width() + 10;
			} else {
				mapHeight = self.mapHeight();
				mapWidth = self.mapWidth();
			}

			socket.emit('shot', {
				hash: window.location.hash,

				// size of the screen to start rendering
				screenHeight: $(document).height(),
				screenWidth: $(document).width(),

				// finished image size
				shotHeight: self.shotHeight(),
				shotWidth: self.shotWidth(),

				// actual dimensions of the map at this screenHeight/screenWidth
				mapHeight: mapHeight,
				mapWidth: mapWidth,

				// other options
				title: self.title(),
				format: self.format(),
				borderless: self.borderLess(),
				// pass on the useragent
				userAgent: navigator.userAgent,
				// papersize for pdf
				paperSize: self.paperSize(),
				// extent pixel size in meters for world file
				extent:  app.map.getExtent().toArray(),
				pixelSize: app.map.getGeodesicPixelSize().w * 1000,
				session: app.session  || null

			}, function (data) {
				self.jobStatus("Job is Complete");
				self.showSpinner(false);
				self.thumbnail(data.thumb);
				self.download(data.download);
			});
		};

		// handle cancel is popover
		self.cancel = function () {
			self.$popover.hide();
		};

		self.url = ko.computed(function () {
		    var url = app.MPSettings.copymachine_endpoint;
            var here = location.protocol + '//' + location.host;
            var printUrl = here + app.viewModel.currentURL() + "&print=true";
            var qs = [];
            var param;

            param = ['url', encodeURIComponent(printUrl)];
            qs.push(param.join('='));

            param = ['title', encodeURIComponent('FooBAR!')];
            qs.push(param.join('='));

            param = ['format', encodeURIComponent(self.format())];
            qs.push(param.join('='));

            if (self.format() == 'pdf') {
                param = ['paper', encodeURIComponent(self.paperSize())];
                qs.push(param.join('='));

                param = ['orientation', encodeURIComponent(self.orientation())];
                qs.push(param.join('='));
            }

            else {
                param = ['width', encodeURIComponent(self.shotWidth())];
                qs.push(param.join('='));
                param = ['height', encodeURIComponent(self.shotHeight())];
                qs.push(param.join('='));
            }

            url = [url, qs.join('&')];
            url = url.join('?');
            return url;
        });
	}
	var shots = {
		$popover: $("#printing-popover")	
	};
	app.viewModel.printing = new printModel(app.map, app.viewModel);
	
	$(document).on('map-ready', function () {
		app.map.events.register('changebaselayer', null, function (event) {
			// console.log('base layer changed');
			app.viewModel.printing.isGoogle(/Google/.test(event.layer.name));
		});

	});
})();
