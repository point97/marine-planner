
// save the initial load hash so we can use it if set
app.hash = window.location.hash;

app.onResize = function() {
	var height = $(window).height() * .60;
	$("#map").height(height);
	$("#data-accordion").height(height);
	$("#legend-accordion").height(height);
	app.map.render('map');
};


// state of the app
app.state = {
	//list of active layer ids in order they appear on the map
	activeLayers: [],
	location: {}
}

// property to store the state of the map for restoring
app.restoreState = {};




ko.applyBindings(app.viewModel);
app.viewModel.loadLayersFromServer();

// initialize the map
app.init();
// Google.v3 uses EPSG:900913 as projection, so we have to
// transform our coordinates
app.map.setCenter(new OpenLayers.LonLat(-69.6, 38).transform(
	new OpenLayers.Projection("EPSG:4326"), new OpenLayers.Projection("EPSG:900913")), 6);		


// if we have the hash state go ahead and load it now
if (app.hash) {
	app.loadStateFromHash(app.hash);
}

$(document).ready(function () {
	app.onResize();
	$(window).resize(app.onResize);
	


	// handle coordinate indicator on pointer
	$('#map').bind('mouseleave mouseenter', function (e) {
		$('#pos').toggle();
	});
	$('#map').bind('mousemove', function (e) {
		$('#pos').css({
			left: e.pageX + 20,
			top: e.pageY + 20
		});
	});       
});

$(document).click(function (e) {
    //removing bookmark popover from view
    if ( e.target.id === "bookmarks-button" ) {
    } else if ( !$(e.target).closest("#bookmark-popover").length ) {
        $('#bookmark-popover').hide();
    }
    
    //removing layer tooltip popover from view
    var layer_pvr_event = $(e.target).closest(".layer-popover").length;
    if ( !layer_pvr_event ) {
        $(".layer-popover").hide();
    }
    
    //removing opacity popover from view
    var op_pvr_event = $(e.target).closest("#opacity-popover").length;
    var op_btn_event = $(e.target).closest(".opacity-button").length;
    //console.log('opacity popover click: ' + op_pvr_event);
    //console.log('opacity button click: ' + op_btn_event);
    if ( !op_pvr_event && !op_btn_event ) {
        //console.log('hiding opacity popover');
        //$('#opacity-popover').hide();
        app.viewModel.hideOpacity();
    }
});
