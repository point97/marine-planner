# Marine Planner

Marine Planner is a lightweight map viewer and data catalog built using Django, Jquery, KnockoutJS, OpenLayers, and Twitter Bootstrap.  Marine Planner is designed to be easily configured and can be readily extended to support a broad range of marine planning activities including visualization, spatial design, and analysis using Madrona and other planning frameworks.

##Features
* Administrative interface for app configuration and management
 * Project name and logo
 * Default map extent and zoom level
 * User account and group management
 * ...and more
* Robust data layer management
 * Full support for OGC and ArcServer REST services (map, legend, feature query)
 * Automatically pull layer titles, descriptions, and supplementary links (metadata, data download, authoritative provider, etc.) or define your own
 * Add and organize layers into categories
 * Support for UTFGrid and GeoJSON layers
 * Filter and format feature query output for each layer
 * Automatic data catalog page built from your layer/category configuration
* Intuitive map interface
 * Layer reordering and opacity adjustment
 * Layer search bar
 * Bookmarks (client side storage)
 * Wide range of basemaps including nautical charts
 * Create map bookmarks and share them with others
 * Embed maps (including bookmarked views) into other pages
 * FullScreen map option
 * Support for tablet and mobile phone devices 
 * Simple Pageguide.js support for showing your users how to use the map

##Installation
NOTE:  These instructions are NOT complete...

To get Marine Planner working on your local machine
* Clone the repository
* Perform the following from the base directory (marine-planner)
* ```vagrant up```
* update your settings_local.py file to include values for
  * ```SECRET_KEY```
  * ```ADMIN_MEDIA_PATH = '/home/vagrant/.virtualenvs/marine-planner/lib/python2.7/site-packages/django/contrib/admin/static/admin/'```
  * ```MEDIA_ROOT = '/home/vagrant/marine-planner/media'```
  * ```MEDIA_URL = '/media/'```
  * ```SOCIAL_AUTH_GOOGLE_PLUS_KEY```
  * ```SOCIAL_AUTH_GOOGLE_PLUS_SECRET```
* ssh into your vagrant box, ```vagrant ssh```, and perform the following
* ```dj syncdb``` (dj can be used as a shortcut 
* ```dj migrate```
* load fixtures or add data for the mp_settings and data_manager app
* ```djrun``` (equivalent to ```python manage.py runserver 0.0.0.0:8000```)

You should now be able to view the site at ```localhost:8000/planner```


##Questions
If you have questions, feature requests, etc, feel free to email us at marine-dev@ecotrust.org

Marine Planner is developed in partnership by Ecotrust and The Nature Conservancy
