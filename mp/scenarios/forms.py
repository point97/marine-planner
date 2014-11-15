from madrona.features.forms import FeatureForm, SpatialFeatureForm
from django import forms
from django.forms import ModelMultipleChoiceField, CheckboxSelectMultiple
from django.forms.widgets import *
from django.forms.widgets import Input
from django.utils.safestring import mark_safe
from django.contrib.gis.geos import fromstr
from os.path import splitext, split
from madrona.analysistools.widgets import SliderWidget, DualSliderWidget
from models import *
from widgets import AdminFileWidget, SliderWidgetWithTooltip, DualSliderWidgetWithTooltip, CheckboxSelectMultipleWithTooltip, CheckboxSelectMultipleWithObjTooltip 

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


class InputWithUnit(Input):
    """Modified Input class that accepts a "unit" parameter, and stores the 
    value in the unit attribute. 
    This is allows additional data associated with a field to be exposed to the 
    template renderer. Later improvements would be to stick this value on the 
    field itself rather than the widget. Also, make it a dictionary rather than
    a single value, so other arbitrary values can be brough forward.   
    """
    def __init__(self, attrs=None, unit=None):
        super(InputWithUnit, self).__init__(attrs)
        self.unit = str(unit)

class TextInputWithUnit(forms.TextInput, InputWithUnit):
    pass

class ScenarioForm(FeatureForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}), required=False)
    
    # Depth Range (meters, avg: 350m - 0m)
    # input_parameter_depth = forms.BooleanField(
    #         widget=CheckboxInput(attrs={'class': 'parameters'}), required=False)
    # input_min_depth = forms.FloatField(initial=10,
    #         widget=forms.TextInput(attrs={'class': 'slidervalue'}))
    # input_max_depth = forms.FloatField(initial=50,
    #         widget=forms.TextInput(attrs={'class': 'slidervalue'}))
    # input_depth = forms.FloatField(
    #     widget=DualSliderWidget('input_min_depth','input_max_depth', min=0,
    #                             max=300, step=1), required=False)
    
    # Distance to Coastline (meters, avg: 17km - 300m)
    input_parameter_coast_distance = forms.BooleanField(
        widget=CheckboxInput(attrs={'class': 'parameters'}), required=False)
    input_min_coast_distance = forms.FloatField(initial=2,
        widget=forms.TextInput(attrs={'class':'slidervalue'}))
    input_max_coast_distance = forms.FloatField(initial=5,
        widget=forms.TextInput(attrs={'class':'slidervalue'}))
    input_coast_distance = forms.FloatField(
        widget=DualSliderWidget('input_min_coast_distance',
                                'input_max_coast_distance', min=0, max=18,
                                step=1), required=False)

    bathy_avg = forms.BooleanField(label="Average Depth",
        widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}), required=False)
    bathy_avg_min = forms.FloatField(initial=10,
        widget=forms.TextInput(attrs={'class':'slidervalue'}))
    bathy_avg_max = forms.FloatField(initial=50,
        widget=TextInputWithUnit(attrs={'class':'slidervalue'}, unit='meters'))
    bathy_avg_input = forms.FloatField(widget=DualSliderWidget('bathy_avg_min', 
                                       'bathy_avg_max', min=1, max=100, step=1))

    wind_avg = forms.BooleanField(widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}), required=False)
    wind_avg_min = forms.FloatField(initial=20,
        widget=forms.TextInput(attrs={'class':'slidervalue'}))
    wind_avg_max = forms.FloatField(initial=40,
        widget=TextInputWithUnit(unit='meters', attrs={'class':'slidervalue'}))
    wind_avg_input = forms.FloatField(widget=DualSliderWidget('wind_avg_min', 
                                     'wind_avg_max', min=1, max=100, step=1))

    subs_avgd = forms.BooleanField(
        widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}), required=False)
    subs_avgd_min = forms.FloatField()
    subs_avgd_max = forms.FloatField(
        widget=TextInputWithUnit(unit='meters', attrs={'class':'slidervalue'}))

    coast_avg = forms.BooleanField(
        widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}), required=False)
    coast_avg_min = forms.FloatField()
    coast_avg_max = forms.FloatField()
    
    mangrove_percent = forms.BooleanField()
    mangrove_min = forms.FloatField()
    mangrove_max = forms.FloatField()
    
    coral_percent = forms.BooleanField()
    coral_min = forms.FloatField()
    coral_max = forms.FloatField()
    
    subveg_percent = forms.BooleanField()
    subveg_min = forms.FloatField()
    subveg_max = forms.FloatField()
    
    protarea_percent = forms.BooleanField()
    protarea_min = forms.FloatField()
    protarea_max = forms.FloatField()
    
    pr_apc_percent = forms.BooleanField()
    pr_apc_min = forms.FloatField()
    pr_apc_max = forms.FloatField()
    
    pr_ape_percent = forms.BooleanField()
    pr_ape_min = forms.FloatField()
    pr_ape_max = forms.FloatField()
    
    vi_apc_percent = forms.BooleanField()
    vi_apc_min = forms.FloatField()
    vi_apc_max = forms.FloatField()
    
    def get_step_1_fields(self):
        """Defines the fields that we want to show on the form in step 1, and 
        the order in which they appear, and in groups of 
            (parameter to test, user-min or user-selection, user-max, user-input)
        where each parameter except the first is optional. 
        """
        names = (('bathy_avg', 'bathy_avg_min', 'bathy_avg_max', 'bathy_avg_input'), 
                 ('wind_avg', 'wind_avg_min', 'wind_avg_max', 'wind_avg_input',),
                 ('subs_avgd', 'subs_avgd_min', 'subs_avgd_max',),
                 ('coast_avg', 'coast_avg_min', 'coast_avg_max',),)

        return self._get_fields(names)

    
    def get_step_2_fields(self):
        """Defines the fields that we want to show on the form in step 2, and 
        the order in which they appear, and in groups of 
            (parameter to test, user-min or user-selection, user-max, user-input)
        where each parameter except the first is optional. 
        """
        names = (('mangrove_percent', 'mangrove_min', 'mangrove_max',),
                ('coral_percent', 'coral_min', 'coral_max',),
                ('subveg_percent', 'subveg_min', 'subveg_max',),
                ('protarea_percent', 'protarea_min', 'protarea_max',),
                ('pr_apc_percent', 'pr_apc_min', 'pr_apc_max',),
                ('pr_ape_percent', 'pr_ape_min', 'pr_ape_max',),
                ('vi_apc_percent', 'vi_apc_min', 'vi_apc_max',),)
        
        return self._get_fields(names)

    def _get_fields(self, names):
        fields = []
        for name_list in names: 
            fields.append([self[name] for name in name_list])
        
        return fields

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
        
        widgets = {
            
        }

