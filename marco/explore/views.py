# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from data_manager.models import *


def data_catalog(request, template='catalog.html'):
    from django.contrib.sites.models import Site
    try:
        domain = Site.objects.all()[0].domain
        if 'localhost' in domain:
            domain = 'http://localhost:8010'
    except:
        domain = '..'
    themes = Theme.objects.all().order_by('name')
    context = {'themes': themes, 'domain': domain}
    return render_to_response(template, RequestContext(request, context)) 

def data_needs(request, template='needs.html'):
    layers = Layer.objects.all().order_by('name')
    context = {'layers': layers}
    return render_to_response(template, RequestContext(request, context)) 
    