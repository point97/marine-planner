(function() {
    function measureModel(map, viewModel) {
        var self = this;
        self.$popover = $('#measure-popover');

        self.toggleMeasureDialog = function(vm, event) {

            // If drawing tool is active, ensure that measure tool is disabled
            if (app.viewModel.scenarios &&
                app.viewModel.scenarios.drawingFormModel &&
                app.viewModel.scenarios.drawingFormModel.isDrawing()) {
                self.cancel();
                return false;
            }

            if (self.$popover.is(":visible")) {
                self.cancel();
            } else {
                app.map.lineMeasure.activate();
                var width = $("#map-panel").width() + $("#legend:visible").width();
                self.$popover.width(width);
                self.$button = $(event.target).closest('.btn');
                self.$popover.show();
            }
        };

        self.meters = ko.observable(0); // Requires OL control to be meters only

        // Metric
        self.units = ko.observable();
        self.roundedDistance = ko.computed(function() {
            var meters = self.meters();
            if (meters > 250) {
                // Convert to km, 2 dec points
                self.units("km");
                return (meters / 1000).toFixed(2);
            } else {
                // Return rounded meters
                self.units("m");
                return meters.toFixed(0);
            }
        });

        // English
        self.unitsEnglish = ko.observable();
        self.roundedDistanceEnglish = ko.computed(function() {
            var meters = self.meters();
            if (meters > 402.366) {
                // 1/4 mi threshold, Convert to mi, 2 dec points
                self.unitsEnglish("mi");
                return (meters / 1609.34).toFixed(2);
            } else {
                // Convert to rounded ft
                self.unitsEnglish("ft");
                return (meters / 0.3048).toFixed(0);
            }
        });

        self.cancel = function() {
            self.$popover.hide();
            self.meters(0);
            app.map.lineMeasure.deactivate();
        };
    }
    app.viewModel.measure = new measureModel(app.map, app.viewModel);
})();
