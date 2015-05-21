from django.db import models
from django.utils.html import escape
from madrona.features import register
from madrona.features.models import PolygonFeature
from madrona.common.utils import LargestPolyFromMulti
from general.utils import sq_meters_to_sq_miles
from ofr_manipulators import clip_to_grid, intersecting_cells
from reports import get_summary_reports, get_chart_values
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver


def cachemethod(cache_key, timeout=60 * 60 * 24 * 7):
    '''
    default timeout = 1 week
    @property
    @cachemethod("SomeClass_get_some_result_%(id)s")
    '''
    def paramed_decorator(func):
        def decorated(self, *args):
            key = cache_key % self.__dict__
            res = cache.get(key)
            if res is None:
                res = func(self, *args)
                cache.set(key, res, timeout)
            return res
        return decorated
    return paramed_decorator

cache_template = "drawing_aoi_%(id)s_serialize_attributes"

@register
class AOI(PolygonFeature):
    description = models.TextField(null=True,blank=True)

    @property
    def formatted_area(self):
        return int((self.area_in_sq_miles * 10) +.5) / 10.

    @property
    def area_in_sq_miles(self):
        return sq_meters_to_sq_miles(self.geometry_final.area)


    @property
    @cachemethod(cache_template)
    def serialize_attributes(self):
        attributes = []
        grid_cells = intersecting_cells(self.geometry_orig)
        attributes.extend(get_summary_reports(grid_cells))
        if self.description:
            attributes.append({'title': 'Description', 'data': self.description})
        report_values = get_chart_values(self.uid, grid_cells)
        return {'event': 'click', 'attributes': attributes, 'report_values': report_values}

    @classmethod
    def fill_color(self):
        return '776BAEFD'

    @classmethod
    def outline_color(self):
        return '776BAEFD'

    def clip_to_grid(self):
        geom = self.geometry_orig
        clipped_shape = clip_to_grid(geom)
        if clipped_shape:
            return LargestPolyFromMulti(clipped_shape)
        else:
            return clipped_shape

    def save(self, *args, **kwargs):
        self.geometry_final = self.clip_to_grid()
        super(AOI, self).save(*args, **kwargs) # Call the "real" save() method

    class Options:
        verbose_name = 'Area of Interest'
        icon_url = 'img/aoi.png'
        export_png = False
        manipulators = []
        # manipulators = ['drawing.manipulators.ClipToPlanningGrid']
        # optional_manipulators = ['clipping.manipulators.ClipToShoreManipulator']
        form = 'drawing.forms.AOIForm'
        form_template = 'aoi/form.html'
        show_template = 'aoi/show.html'


# Signals; handle cache invalidation
@receiver(post_save, sender=AOI)
def postsave_stand_handler(sender, instance, *args, **kwargs):
    key = cache_template % {'id': instance.id}
    cache.delete(key)
    assert cache.get(key) is None
