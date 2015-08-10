from django.db.models import Min, Max
from django.db.models.fields import FloatField, IntegerField
from django.db.models import Q
from django.core.management.base import NoArgsCommand
from pprint import pprint


def model_minmax(klass, nodata=-999):
    """
    for a django model class,
    find the min and max of all numeric fields (Float or Integer)
    optionally exclude a nodata value
    """
    data = {}
    for field in klass._meta.fields:
        if not isinstance(field, FloatField) and not isinstance(field, IntegerField):
            continue
        invfilter = {field.name: nodata}
        n = klass.objects.filter(~Q(**invfilter)).aggregate(Min(field.name)).values()[0]
        x = klass.objects.filter(~Q(**invfilter)).aggregate(Max(field.name)).values()[0]
        data[field.name] = (n, x)

    return data


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        from scenarios.models import GridCell
        pprint(model_minmax(GridCell, -999))
