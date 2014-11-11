from madrona.features.forms import FeatureForm, SpatialFeatureForm
from django import forms
from django.forms import ModelMultipleChoiceField, CheckboxSelectMultiple
from django.forms.widgets import *
from django.utils.safestring import mark_safe
from django.contrib.gis.geos import fromstr
from os.path import splitext, split
from madrona.analysistools.widgets import SliderWidget, DualSliderWidget
from models import *
from widgets import AdminFileWidget, SliderWidgetWithTooltip, DualSliderWidgetWithTooltip, CheckboxSelectMultipleWithTooltip, CheckboxSelectMultipleWithObjTooltip 

WEA_CHOICES = ( ('constrain', 'Constrain the result to the following WEAs'), ('exclude', 'Exclude the following WEAs') )

# http://www.neverfriday.com/sweetfriday/2008/09/-a-long-time-ago.html
class FileValidationError(forms.ValidationError):
    def __init__(self):
        super(FileValidationError, self).__init__('Document types accepted: ' + ', '.join(ValidFileField.valid_file_extensions))
        
class ValidFileField(forms.FileField):
    """A validating document upload field"""
    valid_file_extensions = ['odt', 'pdf', 'doc', 'xls', 'txt', 'csv', 'kml', 'kmz', 'jpeg', 'jpg', 'png', 'gif', 'zip']

    def __init__(self, *args, **kwargs):
        super(ValidFileField, self).__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        f = super(ValidFileField, self).clean(data, initial)
        if f:
            ext = splitext(f.name)[1][1:].lower()
            if ext in ValidFileField.valid_file_extensions: 
                # check data['content-type'] ?
                return f
            raise FileValidationError()

class ScenarioForm(FeatureForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}), required=False)
    
    # GeoPhysical
    input_parameter_depth = forms.BooleanField( widget=CheckboxInput(attrs={'class': 'parameters'}), required=False )
    input_min_depth = forms.FloatField(initial=10, widget=forms.TextInput(attrs={'class':'slidervalue'}))
    input_max_depth = forms.FloatField(initial=50, widget=forms.TextInput(attrs={'class':'slidervalue'}))
    input_depth = forms.FloatField( widget=DualSliderWidget('input_min_depth','input_max_depth',
                                                            min=10,max=100,step=5),
                                    required=False)
                               
#     input_parameter_distance_to_shore = forms.BooleanField( widget=CheckboxInput(attrs={'class': 'parameters'}), required=False )
#     input_min_distance_to_shore = forms.FloatField(initial=12, widget=forms.TextInput(attrs={'class':'slidervalue'}))
#     input_max_distance_to_shore = forms.FloatField(initial=50, widget=forms.TextInput(attrs={'class':'slidervalue'}))
#     input_distance_to_shore = forms.FloatField( widget=DualSliderWidget('input_min_distance_to_shore','input_max_distance_to_shore',
#                                                                         min=3,max=100,step=1),
#                                                 required=False)
#                                          
                                  
    # Wind Energy
    
    #TODO:  might adjust the max_value to 21.5 (this is the max min value, don't yet have the avg value...)                                    
#     input_parameter_wind_speed = forms.BooleanField( widget=CheckboxInput(attrs={'class': 'parameters'}), required=False )
#     input_avg_wind_speed = forms.FloatField(    min_value=7, max_value=9.5, initial=8,
#                                                 #widget=SliderWidgetWithTooltip( min=10,max=21.5,step=.1,
#                                                                                 #id="info_wind_speed_widget"),
#                                                 widget=SliderWidget( min=7,max=9.5,step=.25),
#                                                 required=False )
#                                   
#     input_parameter_distance_to_substation = forms.BooleanField( widget=CheckboxInput(attrs={'class': 'parameters'}), required=False )
#     input_distance_to_substation = forms.FloatField(    min_value=10, max_value=50, initial=30,
#                                                         widget=SliderWidget( min=10,max=50,step=1 ),
#                                                         required=False)
    # Shipping 
                               
    # NON-ACTIVATED FORM ELEMENTS
      
    def save(self, commit=True):
        inst = super(FeatureForm, self).save(commit=False)
        if self.data.get('clear_support_file'):
            inst.support_file = None
        if commit:
            inst.save()
        return inst
    
    class Meta(FeatureForm.Meta):
        model = Scenario
        exclude = list(FeatureForm.Meta.exclude)
        for f in model.output_fields():
            exclude.append(f.attname)


