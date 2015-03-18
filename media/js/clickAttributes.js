
app.clickAttributes = (function() {

	var getSurveyAttributes = function(data, activity) {
		attrs = [];
		if (activity !== 'All Activities') {
			for (var key in data) {
			  	if (data.hasOwnProperty(key) && data[key]) {
			  		if (key === activity) {
			  			if (data[key] === 1) {
			    			attrs.push({'display': key, 'data': data[key] + ' day'});
			  			} else {
			    			attrs.push({'display': key, 'data': data[key] + ' days'});
			  			}
			  		}
			  	}
			}
			attrs.push({'display': 'Total Activity Days (All Activities)', 'data': data['Total Activity Days']});
            // attrs.push({'display': 'UniqueID', 'data': data['UniqueID']});
		} else {
			// for (var key in data) {
			//   	if (data.hasOwnProperty(key) && data[key]) {
			//   		if (key !== 'Total Activity Days' && key !== 'Other' && key !== 'UniqueID') {
			//   			if (data[key] === 1) {
			//     			attrs.push({'display': key, 'data': data[key] + ' day'});
			//   			} else {
			//     			attrs.push({'display': key, 'data': data[key] + ' days'});
			//   			}
			//   		}
			//   	}
			// }
			// // alphabetize and then put Total at top (or bottom)
			// attrs = _.sortBy(attrs, function(obj){ return obj['display']; });
			// if (data['Other']) {
			// 	if (data['Other'] === 1) {
			// 		attrs.push({'display': 'Other', 'data': data['Other'] + ' day'});
			// 	} else {
			// 		attrs.push({'display': 'Other', 'data': data['Other'] + ' days'});
			// 	}
			// }
			attrs.unshift({'display': 'Total Activity Days (All Activities)', 'data': data['Total Activity Days']});
            // attrs.push({'display': 'UniqueID', 'data': data['UniqueID']});
		}
		return attrs;
	};
	
    // Called from utfGridClickHandling in map.js (for Planning Grid click handling)
    var getGridAttributes = function (data) {
        attrs = [];
                
        // Area of mapped Dense Acropora cervicornis patches in m²
        if ('AcervAreaM' in data) {
            attrs.push({'display': 'Mapped Dense Acropora cervicornis', 'data': data['AcervAreaM'].toLocaleString() + ' m&sup2;'});
        }
        // Whether a cell intersects witha designated anchorage
        if ('Anchorage' in data) {
            attrs.push({'display': 'Intersects with a designated anchorage', 'data': data['Anchorage']});
        }
        // Area of Artificial habitats (Sand borrow areas, artificial reefs, inlets , jettys, channels,) in m²
        if ('ArtAreaM' in data) {
            attrs.push({'display': 'Artificial Habitats', 'data': data['ArtAreaM'].toLocaleString() + ' m&sup2;'});
        }
        // 
        if ('BoatUse' in data) {
            attrs.push({'display': 'Boat Use', 'data': data['BoatUse']});
        }
        // 
        if ('CoralCov' in data) {
            attrs.push({'display': 'Coral Cover', 'data': data['CoralCov']});
        }
        // bleaching
        if ('Max_SBII' in data) {
            attrs.push({'display': 'Coral Bleaching', 'data': data['Max_SBII']});
        }
        // Coral Disease
        if ('Max_SDII' in data) {
            attrs.push({'display': 'Coral Disease', 'data': data['Max_SDII']});
        }
        // Coral Density
        if ('Max_ColDen' in data) {
            attrs.push({'display': 'Coral Density', 'data': data['Max_ColDen']});
        }
        // Coral Richness
        if ('Max_N_Taxa' in data) {
            attrs.push({'display': 'Coral Richness', 'data': data['Max_N_Taxa']});
        }
        // Coral Resilience
        if ('Max_RRI_SE' in data) {
            attrs.push({'display': 'Coral Resilience Index', 'data': data['Max_RRI_SE']});
        }
        // 
        if ('CoralSize' in data) {
            attrs.push({'display': 'Coral Size', 'data': data['CoralSize']});
        }
        // 
        if ('County' in data) {
            attrs.push({'display': 'County', 'data': data['County']});
        }
        // 
        if ('DiveUse' in data) {
            attrs.push({'display': 'Dive Use', 'data': data['DiveUse']});
        }
        // Whether a cell intersects with at least one known dense Acropora patches
        if ('DnsAcrpPA' in data) {
            attrs.push({'display': 'Dense Acropora Presence', 'data': data['DnsAcrpPA']});
        }
        // 
        if ('ESAspp' in data) {
            attrs.push({'display': 'ESA Species', 'data': data['ESAspp']});
        }
        // Estimated # of organisms per sq meter
        if ('FishDen' in data) {
            attrs.push({'display': 'Fish Density', 'data': data['FishDen']});
        }
        // 
        if ('FishDiv' in data) {
            attrs.push({'display': 'Fish Diversity', 'data': data['FishDiv']});
        }
        // Estimated # of species per survey area
        if ('FishRich' in data) {
            attrs.push({'display': 'Fish Richness', 'data': data['FishDen']});
        }
        // 
        if ('FishUse' in data) {
            attrs.push({'display': 'Fish Use', 'data': data['FishUse']});
        }
        // Whether a cell intersected with a mapped impact source (artificial reefs, dredged areas, cables, reef injuries, anchorages, burials, etc.)
        if ('Impacted' in data) {
            attrs.push({'display': 'Mapped Impact Source', 'data': data['Impacted']});
        }
        // Whether a cell contains at least one recorded grounding or anchoring event in the DEP database
        if ('InjurySite' in data) {
            attrs.push({'display': 'Recorded Grounding or Anchoring Event', 'data': data['InjurySite']});
        }
        // The distance to the nearest inlet in kilometers
        if ('InletDisMi' in data) {
            attrs.push({'display': 'Distance to Nearest Inlet', 'data': data['InletDisMi'].toFixed(1) + ' mi'});
        }
        // Whether a cell contains at least one known live coral greater than 2 meters in width
        if ('LgLiveCorl' in data) {
            attrs.push({'display': 'Large Live Coral', 'data': data['LgLiveCorl']});
        }
        // 
        if ('Lionfish' in data) {
            attrs.push({'display': 'Lionfish', 'data': data['Lionfish']});
        }
        // 
        if ('MajorHab' in data) {
            attrs.push({'display': 'Majority Habitat', 'data': data['MajorHab']});
        }
        // Depth Range
        if ('MaxDpth_ft' in data && 'MinDpth_ft' in data) {
            attrs.push({'display': 'Depth Range', 'data': data['MinDpth_ft'] + ' to ' + data['MaxDpth_ft'] + ' feet'});
        }
        // Average Depth
        if ('MeanDpth_f' in data) {
            attrs.push({'display': 'Average Depth', 'data': data['MeanDpth_f']});
        }
        // Whether a cell contains at least one Mooring buoy
        if ('MoorngBuoy' in data) {
            attrs.push({'display': 'Mooring Buoy', 'data': data['MoorngBuoy']});
        }
        // The distance to the nearest sewage outfall discharge location in miles
        if ('OutflDisMi' in data) {
            attrs.push({'display': 'Distance to Nearest Outfall', 'data': data['OutflDisMi'].toFixed(1) + ' mi'});
        }
        // The distance to the nearest pier in miles
        if ('PierDisMi' in data) {
            attrs.push({'display': 'Distance to Nearest Pier', 'data': data['PierDisMi'].toFixed(1) + ' mi'});
        }
        // Whether a cell contains at least one recorded Pillar Coral
        if ('PillarPres' in data) {
            attrs.push({'display': 'Pillar Coral Presence', 'data': data['PillarPres']});
        }
        // Percent Artificial substrate (including dump sites, sand borrow areas, outfall pipes and designated artificial reefs) in each planning unit
        if ('PrcntArt' in data) {
            attrs.push({'display': 'Percent Artificial Habitat', 'data': data['PrcntArt']});
        }
        // Percent Reef in each planning unit
        if ('PrcntReef' in data) {
            attrs.push({'display': 'Percent Reef', 'data': data['PrcntReef']});
        }
        // Percent Seagrass in each planning unit
        if ('PrcntSG' in data) {
            attrs.push({'display': 'Percent Seagrass', 'data': data['PrcntSG']});
        }
        // Percent Sand in each planning unit
        if ('PrcntSand' in data) {
            attrs.push({'display': 'Percent Sand', 'data': data['PrcntSand']});
        }
        // 
        if ('RecUse' in data) {
            attrs.push({'display': 'Recreational Use', 'data': data['RecUse']});
        }
        // Area of Coral Reef and Colonized hardbottom habitats in m²
        if ('ReefArea_m' in data) {
            attrs.push({'display': 'Reef Area', 'data': data['ReefArea_m'].toLocaleString() + ' m&sup2;'});
        }
        // 
        if ('Region' in data) {
            attrs.push({'display': 'Region', 'data': data['Region']});
        }
        // Area of Seagrass habitats in m²
        if ('SGarea_m' in data) {
            attrs.push({'display': 'Seagrass Area', 'data': data['SGarea_m'].toLocaleString() + ' m&sup2;'});
        }
        // Area of Sand habitat in m²
        if ('SandArea_m' in data) {
            attrs.push({'display': 'Sand Area', 'data': data['SandArea_m'].toLocaleString() + ' m&sup2;'});
        }
        // The distance to the nearest shore in  kilometers
        if ('ShoreDisMi' in data) {
            attrs.push({'display': 'Distance to Shore', 'data': data['ShoreDisMi'].toFixed(1) + ' mi'});
        }
        // A number assigned to each cell that is unique to the dataset. (no duplicates)
        if ('UniqueID' in data) {
            attrs.push({'display': 'UniqueID (for testing)', 'data': data['UniqueID']});
        }
        // anchor_density
        if ('AncDen0913' in data) {
            attrs.push({'display': 'Anchoring Density', 'data': data['AncDen0913'].toFixed(1) + ' boats'});
        }
        if ('MorDen0913' in data) {
            attrs.push({'display': 'Mooring Density', 'data': data['MorDen0913'].toFixed(1) + ' boats'});
        }
        // Reef fish
        if ('RVCden1213' in data) {
            attrs.push({'display': 'Reef Fish Density',
                        'data': data['RVCden1213'].toFixed(1) + ' units'});
        }
        if ('RVCrch1213' in data) {
            attrs.push({'display': 'Reef Fish Species Richness',
                        'data': data['RVCrch1213'].toFixed(1) + ' units'});
        }
        // Coastal Use survey results
        if ('total_use' in data) {
            attrs.push({'display': 'Total Use Intensity (OFR 2015)',
                        'data': data['total_use'].toFixed(1) + ''});
        }
        if ('boat_use' in data) {
            attrs.push({'display': 'Boater Use Intensity (OFR 2015)',
                        'data': data['boat_use'].toFixed(1) + ''});
        }
        if ('recfish_use' in data) {
            attrs.push({'display': 'Recreational Fishing Use Intensity (OFR 2015)',
                        'data': data['recfish_use'].toFixed(1) + ''});
        }
        if ('scuba_use' in data) {
            attrs.push({'display': 'Scuba Diving Use Intensity (OFR 2015)',
                        'data': data['scuba_use'].toFixed(1) + ''});
        }
        if ('extdive_use' in data) {
            attrs.push({'display': 'Extractive Diving Use Intensity (OFR 2015)',
                        'data': data['extdive_use'].toFixed(1) + ''});
        }
        if ('spear_use' in data) {
            attrs.push({'display': 'Spearfishing Use Intensity (OFR 2015)',
                        'data': data['spear_use'].toFixed(1) + ''});
        }


        return attrs;
    };

    return {
    	getGridAttributes: getGridAttributes,
    	getSurveyAttributes: getSurveyAttributes
    };

})();