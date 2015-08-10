import io
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.contrib.gis.geos import GEOSGeometry, Polygon
from django.template import Context
from django.template.loader import get_template
from madrona.features.models import Feature
from madrona.features import get_feature_by_uid
from simplejson import dumps

from models import *
from drawing.export import geometries_to_shp, zip_objects
from ofr_manipulators import clip_to_grid

def attrs_to_description(attrs):
    # Note: the attributes have raw UTF8 escapes in them
    # ArcMap only seems to recognize caps HTML tags in some special HTML subset
    decoded = ((attr['title'].decode('utf8'), attr['data'].decode('utf8'))
               for attr in attrs)
    lines = ('<DIV><P>%s: %s</P></DIV>' % (k, v)
             for k, v in decoded)
    desc = u'\n'.join(lines)
    return desc

def attrs_to_csv(attrs):
    decoded = ((attr['title'].decode('utf8'), attr['data'].decode('utf8'))
               for attr in attrs)
    lines = (u'"%s","%s"' % (k, v) for k, v in decoded)
    desc = u'\n'.join(lines)
    return desc

def export_shp(request, feature_id):
    """Generate a zipped shape file and return it in a response.
    """
    try:
        drawing = get_feature_by_uid(feature_id)
    except drawing.__class__.DoesNotExist:
        raise Http404()

    if not drawing.user == request.user:
        # if we don't own the drawing, see if it's shared with us
        shared_with_user = drawing.__class__.objects.shared_with_user(request.user)
        shared_with_user = shared_with_user.filter(id=drawing.id)
        if not shared_with_user.exists():
            raise Http404()

    drawing_attributes = drawing.serialize_attributes
    attrs = {'name': drawing.name, 'description': drawing.description}

    try:
        geom = drawing.geometry_final
    except AttributeError:
        # Naturally, planning units have a different field for geometry
        geom = drawing.geometry_dissolved

    items = geometries_to_shp(drawing.name, ((geom, attrs),))

    metadata_file = create_metadata_xml(drawing, drawing_attributes,
                                        items[0]['timestamp'],)
    items.append(metadata_file)

    csv_file = create_csv(drawing, drawing_attributes, items[0]['timestamp'])
    items.append(csv_file)

    zip = zip_objects(items)

    response = HttpResponse(content=zip.read(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=%s.zip' % drawing.name
    return response

def create_csv(drawing, attributes, timestamp):
    try:
        csv = attrs_to_csv(attributes['attributes'])
    except TypeError:
        csv = ''
    csv = csv.encode('utf8')
    csv = io.BytesIO(csv)

    return {
        "timestamp": timestamp,
        "bytes": csv,
        "name": '%s.csv' % drawing.name,
    }


def create_metadata_xml(drawing, attributes, timestamp):
    try:
        description = attrs_to_description(attributes['attributes'])
    except TypeError:
        description = ''

    metadata_context = {
        'title': drawing.name,
        'description': description,
        'summary': drawing.description,
        # 'purpose': '...',
    }
    t = get_template('shape_metadata.xml')
    metadata_xml = t.render(Context(metadata_context))
    metadata_xml = metadata_xml.encode('utf8')
    metadata_xml = io.BytesIO(metadata_xml)

    return {
        "timestamp": timestamp,
        "bytes": metadata_xml,
        "name": '%s.shp.xml' % drawing.name,
    }


'''
'''
def get_drawings(request):
    json = []

    drawings = AOI.objects.filter(user=request.user).order_by('date_created')
    for drawing in drawings:
        sharing_groups = [group.name for group in drawing.sharing_groups.all()]
        try:
            attrs = drawing.serialize_attributes
        except:
            # skip drawing if reports are failing for any reason
            continue  # TODO log errors

        json.append({
            'id': drawing.id,
            'uid': drawing.uid,
            'name': drawing.name,
            'description': drawing.description,
            'attributes': attrs,
            'sharing_groups': sharing_groups
        })

    shared_drawings = AOI.objects.shared_with_user(request.user)
    for drawing in shared_drawings:
        try:
            attrs = drawing.serialize_attributes
        except:
            # skip drawing if reports are failing for any reason
            continue  # TODO log errors

        if drawing not in drawings:
            username = drawing.user.username
            actual_name = drawing.user.first_name + ' ' + drawing.user.last_name
            json.append({
                'id': drawing.id,
                'uid': drawing.uid,
                'name': drawing.name,
                'description': drawing.description,
                'attributes': attrs,
                'shared': True,
                'shared_by_username': username,
                'shared_by_name': actual_name
            })

    return HttpResponse(dumps(json))

'''
'''
def delete_drawing(request, uid):
    try:
        drawing_obj = get_feature_by_uid(uid)
    except Feature.DoesNotExist:
        raise Http404

    #check permissions
    viewable, response = drawing_obj.is_viewable(request.user)
    if not viewable:
        return response

    drawing_obj.delete()

    return HttpResponse("", status=200)

'''
'''
def get_clipped_shape(request):
    zero = .01

    if not (request.POST and request.POST['target_shape']):
        return HTTPResponse("No shape submitted", status=400)

    target_shape = request.POST['target_shape']
    geom = GEOSGeometry(target_shape, srid=3857)

    clipped_shape = clip_to_grid(geom)

    # return new_shape['geometry__union']
    if clipped_shape and clipped_shape.area >= zero: #there was overlap
        largest_poly = LargestPolyFromMulti(clipped_shape)
        wkt = largest_poly.wkt
        return HttpResponse(dumps({"clipped_wkt": wkt}), status=200)
    else:
        return HttpResponse("Submitted Shape is outside Grid Cell Boundaries (no overlap).", status=400)

    # return HttpResponse(dumps({"clipped_wkt": wkt}), status=200)


'''
'''
def aoi_analysis(request, aoi_id):
    from aoi_analysis import display_aoi_analysis
    aoi_obj = get_object_or_404(AOI, pk=aoi_id)
    #check permissions
    viewable, response = aoi_obj.is_viewable(request.user)
    if not viewable:
        return response
    return display_aoi_analysis(request, aoi_obj)
    # Create your views here.


def get_attributes(request, uid):
    try:
        scenario_obj = get_feature_by_uid(uid)
    except Scenario.DoesNotExist:
        raise Http404

    # check permissions
    viewable, response = scenario_obj.is_viewable(request.user)
    if not viewable:
        return response

    return HttpResponse(dumps(scenario_obj.serialize_attributes))

'''
'''
def get_geometry_orig(request, uid):
    try:
        scenario_obj = get_feature_by_uid(uid)
        wkt = scenario_obj.geometry_orig.wkt
    except Scenario.DoesNotExist:
        raise Http404

    #check permissions
    viewable, response = scenario_obj.is_viewable(request.user)
    if not viewable:
        return response

    return HttpResponse(dumps({"geometry_orig": wkt}), status=200)


'''
'''
# def wind_analysis(request, wind_id):
#     from wind_analysis import display_wind_analysis
#     wind_obj = get_object_or_404(WindEnergySite, pk=wind_id)
#     #check permissions
#     viewable, response = wind_obj.is_viewable(request.user)
#     if not viewable:
#         return response
#     return display_wind_analysis(request, wind_obj)
#     # Create your views here.
