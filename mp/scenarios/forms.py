# coding: utf-8
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
    # Boolean field is the anchor, and used as the base name for rendering the
    # form. 
    # - Help_text on the boolean is included in the popup text "info" icon.
    # - Label is used as the icon label 
    bathy_avg = forms.BooleanField(label="Average Depth",
        widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}), 
        help_text="Average bathymetric depth (meters)")
    bathy_avg_min = forms.FloatField(initial=10,
        widget=forms.TextInput(attrs={'class':'slidervalue'}))
    bathy_avg_max = forms.FloatField(initial=50,
        widget=TextInputWithUnit(attrs={'class':'slidervalue'}, unit='meters'))
    bathy_avg_input = forms.FloatField(widget=DualSliderWidget('bathy_avg_min', 
                                       'bathy_avg_max', min=1, max=300, step=1))

    # Wind range 72 - 400 W/m^2
    wind_avg = forms.BooleanField(label="Wind energy potential",
                                  help_text="Wind energy generation potential (watts per square meter).", 
        widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    wind_avg_min = forms.FloatField(initial=200, required=False,
        widget=forms.TextInput(attrs={'class':'slidervalue'}))
    wind_avg_max = forms.FloatField(initial=400, required=False,
        widget=TextInputWithUnit(unit='W/m²', attrs={'class':'slidervalue'}))
    wind_avg_input = forms.FloatField(required=False, widget=DualSliderWidget('wind_avg_min', 
                                     'wind_avg_max', min=72, max=400, step=1))

    subs_mind = forms.BooleanField(label="Substation distance", 
        help_text="Distance to a power substation (meters).",
        widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    subs_mind_min = forms.FloatField(required=False, initial=425)
    subs_mind_max = forms.FloatField(required=False, initial=15000,
        widget=TextInputWithUnit(unit='meters', attrs={'class':'slidervalue'}))
    subs_mind_input = forms.FloatField(widget=DualSliderWidget('subs_mind_min', 
                                     'subs_mind_max', min=425, max=108430, step=1))

    coast_avg = forms.BooleanField(label="Coastline Distance",  
        help_text="Average distance to coastline (meters).",
        widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    coast_avg_min = forms.FloatField(required=False, initial=380)
    coast_avg_max = forms.FloatField(required=False, initial=10000)
    coast_avg_input = forms.FloatField(widget=DualSliderWidget('coast_avg_min', 
                                     'coast_avg_max', min=380, max=17845, step=1))

    mangrove_p = forms.BooleanField(label="Mangrove %",
        widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    mangrove_p_min = forms.FloatField(required=False, initial=0)
    mangrove_p_max = forms.FloatField(required=False, initial=50)
    mangrove_p_input = forms.FloatField(required=False, 
        widget=DualSliderWidget('mangrove_p_min', 'mangrove_p_max', 
                                min=0, max=100, step=1))
    
    coral_p = forms.BooleanField(label="Coral %", 
        widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}), required=False)
    coral_p_min = forms.FloatField(required=False, initial=0)
    coral_p_max = forms.FloatField(required=False, initial=50)
    coral_p_input = forms.FloatField(required=False, 
        widget=DualSliderWidget('coral_p_min', 'coral_p_max', 
                                min=0, max=100, step=1))

    subveg_p = forms.BooleanField(label="Subveg %",
        widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}), required=False)
    subveg_p_min = forms.FloatField(required=False, initial=0)
    subveg_p_max = forms.FloatField(required=False, initial=50)
    subveg_p_input = forms.FloatField(required=False, 
        widget=DualSliderWidget('subveg_p_min', 'subveg_p_max', 
                                min=0, max=100, step=1))

    protarea_p = forms.BooleanField(label="Prot Area %",
        widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    protarea_p_min = forms.FloatField(required=False, initial=0)
    protarea_p_max = forms.FloatField(required=False, initial=50)
    protarea_p_input = forms.FloatField(required=False, 
        widget=DualSliderWidget('protarea_p_min', 'protarea_p_max', 
                                min=0, max=100, step=1))

    pr_apc_p = forms.BooleanField(label="PR APC %", 
        widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    pr_apc_p_min = forms.FloatField(required=False, initial=0)
    pr_apc_p_max = forms.FloatField(required=False, initial=50)
    pr_apc_p_input = forms.FloatField(required=False, 
        widget=DualSliderWidget('pr_apc_p_min', 'pr_apc_p_max', 
                                min=0, max=100, step=1))

    pr_ape_p = forms.BooleanField(label="PR APE %",
        widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    pr_ape_p_min = forms.FloatField(required=False, initial=0)
    pr_ape_p_max = forms.FloatField(required=False, initial=50)
    pr_ape_p_input = forms.FloatField(required=False, 
        widget=DualSliderWidget('pr_ape_p_min', 'pr_ape_p_max', 
                                min=0, max=100, step=1))

    vi_apc_p = forms.BooleanField(label="VI APC %",
        widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    vi_apc_p_min = forms.FloatField(required=False, initial=0)
    vi_apc_p_max = forms.FloatField(required=False, initial=50)
    vi_apc_p_input = forms.FloatField(required=False, 
        widget=DualSliderWidget('vi_apc_p_min', 'vi_apc_p_max', 
                                min=0, max=100, step=1))
    
    def get_step_1_fields(self):
        """Defines the fields that we want to show on the form in step 1, and 
        the order in which they appear, and in groups of 
            (parameter to test, user-min or user-selection, user-max, user-input)
        where each parameter except the first is optional. 
        """
        names = (('bathy_avg', 'bathy_avg_min', 'bathy_avg_max', 'bathy_avg_input'), 
                 ('wind_avg', 'wind_avg_min', 'wind_avg_max', 'wind_avg_input',),
                 ('subs_mind', 'subs_mind_min', 'subs_mind_max', 'subs_mind_input',),
                 ('coast_avg', 'coast_avg_min', 'coast_avg_max', 'coast_avg_input', ),)

        return self._get_fields(names)

    
    def get_step_2_fields(self):
        """Defines the fields that we want to show on the form in step 2, and 
        the order in which they appear, and in groups of 
            (parameter to test, user-min or user-selection, user-max, user-input)
        where each parameter except the first is optional. 
        """
        names = (('mangrove_p', 'mangrove_p_min', 'mangrove_p_max', 'mangrove_p_input',),
                ('coral_p', 'coral_p_min', 'coral_p_max', 'coral_p_input',),
                ('subveg_p', 'subveg_p_min', 'subveg_p_max', 'subveg_p_input',),
                ('protarea_p', 'protarea_p_min', 'protarea_p_max', 'protarea_p_input',),
                ('pr_apc_p', 'pr_apc_p_min', 'pr_apc_p_max', 'pr_apc_p_input',),
                ('pr_ape_p', 'pr_ape_p_min', 'pr_ape_p_max', 'pr_ape_p_input',),
                ('vi_apc_p', 'vi_apc_p_min', 'vi_apc_p_max', 'vi_apc_p_input',))
        
        return self._get_fields(names)

    def get_steps(self):
        return self.get_step_1_fields(), self.get_step_2_fields()

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

