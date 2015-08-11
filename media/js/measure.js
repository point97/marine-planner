(function() {
    function measureModel(map, viewModel) {
        var self = this;
        self.$popover = $('#measure-popover');

        self.toggleMeasureDialog = function(vm, event) {
            app.map.lineMeasure.activate();
            var width = $("#map-panel").width() + $("#legend:visible").width();
            self.$popover.width(width);
            self.$button = $(event.target).closest('.btn');
            if (self.$popover.is(":visible")) {
                self.cancel();
            } else {
                self.$popover.show();
            }
        };

        self.distance = ko.observable(0);
        self.units = ko.observable();
        self.roundedDistance = ko.computed(function() {
            var units = self.units();
            if (units == 'mi' || units == 'km') {
                return self.distance().toFixed(2);
            } else if (units == 'ft' || units == 'm') {
                return self.distance().toFixed(0);
            } else {
                return self.distance();
            }
        });
        self.cancel = function() {
            self.$popover.hide();
            self.distance(0);
            app.map.lineMeasure.deactivate();
        };
        self.doPrint = function() {
            $("#measure-modal").modal('show');
            return true;
        };
    }
    app.viewModel.measure = new measureModel(app.map, app.viewModel);
})();
