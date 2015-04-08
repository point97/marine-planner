# Updating OFR with new planning grids

## Inspect shapefile

 Check out the delivered shapefile with `ogrinfo` and/or `qgis` to make sure everything is in web mercator and generally checks out. Cross check that with the [OFR Grid Attributes](https://docs.google.com/spreadsheets/d/1LOT9xl6_iiUSCI09_al7phZDF50HSnPPZRp768R1Xyg/edit?pli=1#gid=0) spreadsheet and identify changes marked in red.

## Edit files to reflect the new schema

* `scripts/field_map.json`: keys are the lowercase fieldname from the shapefile, values are the internal name used in python/js code.

* `mp/scenarios/models.py`: modify the `GridCell` class to make sure all attributes are reflected in the schema.

#### **If** the attribute is used for filtering:

* `mp/scenarios/models.py`: Modify the `Scenario` class with all filterable fields. There will be a boolean field named after the internal name and a series of other fields (`*_input`, `*_min`, `*_max`) depending on whether the data is categorical or a numeric slider.
* `mp/scenarios/models.py`: Modify the `serialize_attributes` method of the `Scenario` class to contain all relevant attributes. This controls the info content when clicking on existing designs.
* `mp/scenarios/forms.py`: modify the `ScenarioForm`
* `mp/scenarios/forms.py`: modify the appropriate `get_step_*_fields` and ensure the attribute shows up on the correct page in the proper order.
* `mp/scenarios/views.py`: add filtering logic for all fields to `run_filter_query`
* `media/js/scenarios.js`: add knockout observables to the `ScenarioFormModel`
* `media/js/scenarios.js`: add the internal names to the `parameters` Array

#### If the attribute is to be reported on the gridcell click info:
* `media/js/clickAttributes.js`: modify the `getGridAttributes` function for UTFGrid callbacks. Keep in mind that this uses the case-sensitive field name from the original shapefile!

#### If the attribute is to be included in summary reports for drawings:
* `mp/drawing/reports.py`: modify the `get_summary_reports` function as needed.

## Create a SQL file and load new gridcell data

Modify the `scripts/process_grid.sh` script, should be only the `SHP` and `FINAL` variables that need attention.

Run the script from your virtual machine; outputs a sql file.

    bash scripts/process_grid.sh

Load the sql file output by this script into your local dev postgis database. This will drop and completely recreate your gridcell table with the new data command like:

    psql -U postgres -d marco -f ofr_planning_grid.sql

Note that, at this point, we have manually created a postgres table for the `scenario.GridCell` model so it does not need migrations. Unfortunately the `scenario.Scenario` model does. Since we can only do migrations on an app basis (not by model) we'll need to create the migration and manually remove the migration code related to gridcells. From the VM dev server

    dj schemamigration --auto scenarios

Then open the `mp/scenarios/migrations/<migration>.py` file and delete all actions related to the `scenarios_gridcell` table from both the `forwards` and `backwards` methods.

Finally, apply the migrations locally and commit them to the repo.

    dj migrate scenarios

Finally, test and update/check the google docs spreadsheet

## Generate mbtiles:

Taken mostly from [Scott's docs](https://sites.google.com/a/pointnineseven.com/scott-s-notes/apps/our-florida-reefs-mp#mbtiles) and modified slightly.

Create a NEW OFR_Planning_Grid project in TileMill

Load shapefile

Zoom to layer extent (magnifying icon in Layers list)

Style the grid

    #ofr-planning-grid {
      ::outline {
        line-color: #888;
        line-width: 1;
        line-opacity: .5;
      }
      polygon-opacity: 0;
    }

Add interactivity attributes. Verify that the attributes show up on mouseover within TileMill (might have to hit Save)

Export MBTiles

    zooming to level 14 for now (level 16 took a couple hours, but will be what we want at some point - level 14 takes less than a minute at 7MB)
    Center:  -80.0642,26.4558,9
    Bounds:  -80.1686,25.5573,-79.9709,27.2766

Save to local drive

    OFR_Planning_Grid_20150406b.mbtiles

Move to util server, overwriting the master OFR_Planning_Grid layer. If you want to test it out, just name it something other than `OFR_Planning_Grid.mbtiles` which should be considered the "production" layer.

    scp OFR_Planning_Grid_20150406b.mbtiles util:/var/apps/mbtiles/OFR_Planning_Grid.mbtiles

Tiles json should now be available via

    http://util.point97.io/tiles/OFR_Planning_Grid.json

Update the layer via the django admin (URL and UTFURL fields)

Verify Planning Grid on the tool and via the following URLs

    http://util.point97.io/tiles/OFR_Planning_Grid/14/4548/6946.png
    http://util.point97.io/tiles/OFR_Planning_Grid/14/4548/6946.grid.json



## Deployment

First, note that code migrations must happen at precisely the same time as the new gridcell data is loaded. It's probably safest to shut down the app server or put it in maintenance mode while performing the deployment.

Load the gridcell data into the production database, password is on the ofr server in local settings

    psql -h database.point97.io -U ofr -d ofr -f /tmp/ofr_planning_grid_13Mar2015.sql

Then ssh into the ofr production server, pull code and run migrations

    ssh ofr
    source env/ofr/bin/activate
    cd webapps/marine_planner

    git fetch
    git reset -q --hard origin/ofr

    python manage.py migrate

Restart the app server and test away. It would not hurt to again refer to the google docs spreadsheet and check that all issues have been addressed.