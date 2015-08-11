(function() {
    function measureModel(map, viewModel) {
        var self = this;
        self.$popover = $('#measure-popover');

        self.showMeasureDialog = function(vm, event) {
            app.map.lineMeasure.activate();
            var width = $("#map-panel").width() + $("#legend:visible").width();
            self.$popover.width(width);
            self.$button = $(event.target).closest('.btn');
            if (self.$popover.is(":visible")) {
                self.$popover.hide();
            } else {
                self.$popover.show();
            }
        };

        // working dimensions of map for rendering purposes
        self.distance = ko.observable(0);
        self.roundedDistance = ko.computed(function() {
            return self.distance().toFixed(3);
        });
        self.units = ko.observable();
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
