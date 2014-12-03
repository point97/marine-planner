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
    bathy_avg = forms.BooleanField(label="Average Depth", required=False,
        widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}), 
        help_text="Average bathymetric depth (meters)")
    bathy_avg_min = forms.FloatField(initial=10,
        widget=forms.TextInput(attrs={'class':'slidervalue'}))
    bathy_avg_max = forms.FloatField(initial=50,
        widget=TextInputWithUnit(attrs={'class':'slidervalue'}, unit='meters'))
    bathy_avg_input = forms.FloatField(widget=DualSliderWidget('bathy_avg_min', 
                                       'bathy_avg_max', min=1, max=300, step=1))

    # Wind range 72 - 400 W/m^2
    wind_avg = forms.BooleanField(label="Wind energy potential", required=False,
                                  help_text="Minimum wind energy generation potential (watts per square meter).", 
        widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    wind_avg_min = forms.FloatField(initial=200, required=False,
        widget=SliderWidget(attrs={'class':'slidervalue'}, min=72, max=400, 
                            step=1))

    subs_mind = forms.BooleanField(label="Substation distance", required=False,
        help_text="Maximum distance to a power substation (meters).",
        widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    subs_mind_max = forms.FloatField(required=False, initial=15000,
        widget=SliderWidget(attrs={'class':'slidervalue'}, 
                            min=425, max=108430, step=1))

    coast_avg = forms.BooleanField(label="Coastline Distance", required=False,
        help_text="Average distance to coastline (meters).",
        widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    coast_avg_min = forms.FloatField(required=False, initial=380)
    coast_avg_max = forms.FloatField(required=False, initial=10000)
    coast_avg_input = forms.FloatField(widget=DualSliderWidget('coast_avg_min', 
                                     'coast_avg_max', min=380, max=17845, step=1))

    mangrove_p = forms.BooleanField(label="Mangroves", required=False,
        widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    
    coral_p = forms.BooleanField(label="Corals", required=False,
        widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))

    subveg_p = forms.BooleanField(label="Submerged Vegetation", required=False,
        widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))

    protarea_p = forms.BooleanField(label="Protected Areas", required=False,
        widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))

    pr_apc_p = forms.BooleanField(label="PR Conservation Priority Areas", required=False,
        widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))

    pr_ape_p = forms.BooleanField(label="PR Special Planning Areas", required=False,
        widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))

    vi_apc_p = forms.BooleanField(label="USVI Areas of Particular Concern", required=False,
        widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    
    def get_step_1_fields(self):
        """Defines the fields that we want to show on the form in step 1, and 
        the order in which they appear, and in groups of 
            (parameter to test, user-min or user-selection, user-max, user-input)
        where each parameter except the first is optional. 
        """
        names = (('bathy_avg', 'bathy_avg_min', 'bathy_avg_max', 'bathy_avg_input'), 
                 ('wind_avg', 'wind_avg_min', None,), 
                 ('subs_mind', None, 'subs_mind_max',),
                 ('coast_avg', 'coast_avg_min', 'coast_avg_max', 'coast_avg_input', ),)

        return self._get_fields(names)

    
    def get_step_2_fields(self):
        """Defines the fields that we want to show on the form in step 2, and 
        the order in which they appear, and in groups of 
            (parameter to test, user-min or user-selection, user-max, user-input)
        where each parameter except the first is optional. 
        """
        names = (('mangrove_p', None, None, None,),
                ('coral_p', None, None, None,),
                ('subveg_p', None, None, None,),
                ('protarea_p', None, None, None,),
                ('pr_apc_p', None, None, None,),
                ('pr_ape_p', None, None, None,),
                ('vi_apc_p', None, None, None,),)
        
        return self._get_fields(names)

    def get_steps(self):
        return self.get_step_1_fields(), self.get_step_2_fields()

    def _get_fields(self, names):
        fields = []
        for name_list in names: 
            group = []
            for name in name_list: 
                if name:
                    group.append(self[name])
                else:
                    group.append(None)
            fields.append(group)
        return fields

      
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

