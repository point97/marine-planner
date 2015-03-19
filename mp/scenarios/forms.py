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
    
    # Depth Range (meters, avg: 0m - 212m)
    # Boolean field is the anchor, and used as the base name for rendering the form. 
    # - Help_text on the boolean is included in the popup text "info" icon.
    # - Label is used as the icon label 
    depth = forms.BooleanField(label="Average Depth", required=False, help_text="The average depth in a planning unit in ft. Positive sign indicates depth, negative indicates elevation", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    # depth_min = forms.FloatField(required=False, initial=10, widget=SliderWidget(attrs={'class':'slidervalue', 'pre_text': 'Distance in meters', 'post_text': 'meters'}, min=1, max=220, step=1))
    depth_min = forms.FloatField(required=False, initial=10, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': 'Depth Range (feet)'}))
    depth_max = forms.FloatField(required=False, initial=50, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': 'to'}))
    depth_input = forms.FloatField(widget=DualSliderWidget('depth_min', 'depth_max', min=1, max=220, step=1))

    shore_distance = forms.BooleanField(label="Distance to Shore", required=False, help_text="Distance to nearest shore in miles", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    shore_distance_min = forms.FloatField(required=False, initial=3, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': 'Distance (in mi)'}))
    shore_distance_max = forms.FloatField(required=False, initial=10, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': 'to'}))
    # shore_distance_max = forms.FloatField(required=False, initial=10000, widget=TextInputWithUnit(attrs={'class':'slidervalue'}, unit='meters'))
    shore_distance_input = forms.FloatField(widget=DualSliderWidget('shore_distance_min', 'shore_distance_max', min=0, max=13, step=.5))

    pier_distance = forms.BooleanField(label="Distance to Pier", required=False, help_text="Distance to nearest pier in miles", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox', 'layer_id': 326, 'layer_title': 'Show Pier Locations'}))
    pier_distance_min = forms.FloatField(required=False, initial=5, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': 'Distance in miles'}))
    pier_distance_max = forms.FloatField(required=False, initial=20, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': 'to'}))
    pier_distance_input = forms.FloatField(widget=DualSliderWidget('pier_distance_min', 'pier_distance_max', min=0, max=35, step=.5))

    inlet_distance = forms.BooleanField(label="Distance from Coastal Inlet", required=False, help_text="Distance to nearest inlet in miles", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox', 'layer_id': 339, 'layer_title': 'Show Inlets and Passes'}))
    inlet_distance_min = forms.FloatField(required=False, initial=3, widget=SliderWidget(attrs={'class':'slidervalue', 'range': 'max', 'pre_text': 'Exclusion Buffer (in mi)', 'post_text': 'mi'}, min=0, max=16, step=.5))

    outfall_distance = forms.BooleanField(label="Distance from Outfall", required=False, help_text="Distance from nearest sewage outfall discharge location in miles", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox', 'layer_id': 350, 'layer_title': 'Show Outfall Locations'}))
    outfall_distance_min = forms.FloatField(required=False, initial=2, widget=SliderWidget(attrs={'class':'slidervalue', 'range': 'max', 'pre_text': 'Exclusion Buffer (in mi)', 'post_text': 'mi'}, min=0, max=10, step=.5))


    injury_site = forms.BooleanField(label="Injury Sites", required=False, help_text="Planning units that contain at least one known location of past grounding, anchoring, cable, or other reef injury event (FDEP database)", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox', 'layer_id': '328', 'layer_title': 'Show Reef Injury Sites'}))
    injury_site_input = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'parameters', 'layer_id': '918', 'layer_title': 'Reef Injury Site'}), choices=(('Y', 'Include'), ('N', 'Exclude')), initial='Y')

    large_live_coral = forms.BooleanField(label="Large Live Corals", required=False, help_text="Planning units that contain at least one known live coral greater than 2m.", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    large_live_coral_input = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'parameters'}), choices=(('Y', 'Include'), ('N', 'Exclude')), initial='Y')

    pillar_presence = forms.BooleanField(label="Pillar Corals", required=False, help_text="Planning units that contain at least one known pillar coral. (FWC database)", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox', 'layer_id': 309, 'layer_title': 'Show Pillar Coral Sites'}))
    pillar_presence_input = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'parameters'}), choices=(('P', 'Include'), ('A', 'Exclude')), initial='Y')

    anchorage = forms.BooleanField(label="Anchorage Areas", required=False, help_text="Planning units that overlap presently designated anchorages.", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox', 'layer_id': 334, 'layer_title': 'Show Commercial Anchorage Areas'}))
    anchorage_input = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'parameters'}), choices=(('Y', 'Include'), ('N', 'Exclude')), initial='Y')

    mooring_buoy = forms.BooleanField(label="Mooring Buoys", required=False, help_text="Planning units that contain at least one mooring buoy.", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox', 'layer_id': 360, 'layer_title': 'Show Mooring Buoys'}))
    mooring_buoy_input = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'parameters'}), choices=(('Y', 'Include'), ('N', 'Exclude')), initial='Y')

    impacted = forms.BooleanField(label="Mapped Impact Source", required=False, help_text="Planning units that contain at least one known planned or unplanned impact including injury sites, artificial reefs and substrate, outfalls, piers, cables, tires, inlets, channels, dredged areas, spoil areas, and/or commercial ship anchorages.", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    impacted_input = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'parameters'}), choices=(('Y', 'Include'), ('N', 'Exclude')), initial='Y')

    acropora_pa = forms.BooleanField(label="Dense Acropora Present", required=False, help_text="Planning units that contain at least part of a known dense Acropora patch.", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    acropora_pa_input = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'parameters'}), choices=(('Y', 'Include'), ('N', 'Exclude')), initial='Y')

    # acropora_pa = forms.BooleanField(label="Acropora Presence / Absence", required=False, help_text="Select cells based on Presence or Absence", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    # acropora_pa_input = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'parameters'}), choices=(('A', 'Absence'), ('P', 'Presence')), initial='A')
    # Giving up on RadioSelect, it refused to return anything other than the last choice as the selection to the server...Select widget seems to work fine through...


    prcnt_sg = forms.BooleanField(label="Percent Seagrass", required=False, help_text="Minimum percent of mapped seagrass area within each planning unit", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox', 'layer_id': 318, 'layer_title': 'Show Seagrass Habitats'}))
    prcnt_sg_min = forms.FloatField(required=False, initial=30, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': 'Minimum Percentage'}))
    prcnt_sg_max = forms.FloatField(required=False, initial=50, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': 'to'}))
    prcnt_sg_input = forms.FloatField(widget=DualSliderWidget('prcnt_sg_min', 'prcnt_sg_max', min=0, max=100, step=10))

    prcnt_reef = forms.BooleanField(label="Percent Reef", required=False, help_text="Minimum percent of mapped reef area within each planning unit", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    prcnt_reef_min = forms.FloatField(required=False, initial=30, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': 'Minimum Percentage'}))
    prcnt_reef_max = forms.FloatField(required=False, initial=50, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': 'to'}))
    prcnt_reef_input = forms.FloatField(widget=DualSliderWidget('prcnt_reef_min', 'prcnt_reef_max', min=0, max=100, step=10))

    prcnt_sand = forms.BooleanField(label="Percent Sand", required=False, help_text="Minimum percent of mapped sand area within each planning unit", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    prcnt_sand_min = forms.FloatField(required=False, initial=30, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': 'Minimum Percentage'}))
    prcnt_sand_max = forms.FloatField(required=False, initial=50, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': 'to'}))
    prcnt_sand_input = forms.FloatField(widget=DualSliderWidget('prcnt_sand_min', 'prcnt_sand_max', min=0, max=100, step=10))

    prcnt_art = forms.BooleanField(label="Percent Artificial Substrate", required=False, help_text="Minimum percent of mapped artificial substrate area (including dump sites, outfall pipes and designated artificial reefs) within each planning unit", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    prcnt_art_min = forms.FloatField(required=False, initial=30, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': 'Minimum Percentage'}))
    prcnt_art_max = forms.FloatField(required=False, initial=50, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': 'to'}))
    prcnt_art_input = forms.FloatField(widget=DualSliderWidget('prcnt_art_min', 'prcnt_art_max', min=0, max=100, step=10))

    fish_richness = forms.BooleanField(label="Fish Richness", required=False, help_text="Minimum estimated species count per survey area", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    fish_richness_max = forms.FloatField(required=False, initial=15, widget=SliderWidget(attrs={'class':'slidervalue', 'range': 'max'}, min=0, max=40, step=5))

    coral_richness = forms.BooleanField(label="Coral Richness", required=False, help_text="Number of coral species (FRRP data)", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    coral_richness_min = forms.FloatField(required=False, initial=5, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': ''}))
    coral_richness_max = forms.FloatField(required=False, initial=50, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': 'to'}))
    coral_richness_input = forms.FloatField(widget=DualSliderWidget('coral_richness_min', 'coral_richness_max', min=0, max=100, step=1))

    coral_density = forms.BooleanField(label="Coral Density", required=False, help_text="Number of coral colonies per square meter (FRRP data)", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    coral_density_min = forms.FloatField(required=False, initial=2, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': ''}))
    coral_density_max = forms.FloatField(required=False, initial=50, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': 'to', 'post_text': 'per sq. meter'}))
    coral_density_input = forms.FloatField(widget=DualSliderWidget('coral_density_min', 'coral_density_max', min=0, max=100, step=1))

    coral_bleach = forms.BooleanField(label="Coral Bleaching", required=False, help_text="Coral site bleaching index", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    coral_bleach_min = forms.FloatField(required=False, initial=2, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': ''}))
    coral_bleach_max = forms.FloatField(required=False, initial=50, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': 'to'}))
    coral_bleach_input = forms.FloatField(widget=DualSliderWidget('coral_bleach_min', 'coral_bleach_max', min=0, max=100, step=1))

    coral_disease = forms.BooleanField(label="Coral Disease", required=False, help_text="Coral site disease index", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    coral_disease_min = forms.FloatField(required=False, initial=2, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': ''}))
    coral_disease_max = forms.FloatField(required=False, initial=50, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': 'to'}))
    coral_disease_input = forms.FloatField(widget=DualSliderWidget('coral_disease_min', 'coral_disease_max', min=0, max=100, step=1))

    coral_resilience = forms.BooleanField(label="Coral Resilience Index", required=False, help_text="Coral resilience index", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    coral_resilience_min = forms.FloatField(required=False, initial=0, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': ''}))
    coral_resilience_max = forms.FloatField(required=False, initial=50, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': 'to'}))
    coral_resilience_input = forms.FloatField(widget=DualSliderWidget('coral_resilience_min', 'coral_resilience_max', min=0, max=100, step=1))

    reef_fish_density = forms.BooleanField(label="Reef Fish Density", required=False, help_text="Number of fish species per PSU (RVC 2012 & 2013)", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    reef_fish_density_min = forms.FloatField(required=False, initial=10, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': ''}))
    reef_fish_density_max = forms.FloatField(required=False, initial=50, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': 'to'}))
    reef_fish_density_input = forms.FloatField(widget=DualSliderWidget('reef_fish_density_min', 'reef_fish_density_max', min=0, max=100, step=1))

    reef_fish_richness = forms.BooleanField(label="Reef Fish Species Richness", required=False, help_text="Mean fish density per PSU (RVC 2012 & 2013)", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    reef_fish_richness_min = forms.FloatField(required=False, initial=5, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': ''}))
    reef_fish_richness_max = forms.FloatField(required=False, initial=50, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': 'to'}))
    reef_fish_richness_input = forms.FloatField(widget=DualSliderWidget('reef_fish_richness_min', 'reef_fish_richness_max', min=0, max=100, step=1))

    # coral_p = forms.BooleanField(label="Corals", required=False, help_text="Coral cover", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    # mangrove_p = forms.BooleanField(label="Mangroves", required=False, help_text="Mangrove cover", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))

    total_use = forms.BooleanField(label="Total Use Intensity", required=False, help_text="Planning units that contain at least one entry in the 2015 OFR survey", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    total_use_min = forms.FloatField(required=False, initial=5, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': ''}))
    total_use_max = forms.FloatField(required=False, initial=50, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': 'to'}))
    total_use_input = forms.FloatField(widget=DualSliderWidget('total_use_min', 'total_use_max', min=0, max=100, step=1))

    boat_use = forms.BooleanField(label="Boater Use Intensity", required=False, help_text="Planning units that contain at least one entry for boating in the 2015 OFR survey", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    boat_use_min = forms.FloatField(required=False, initial=5, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': ''}))
    boat_use_max = forms.FloatField(required=False, initial=50, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': 'to'}))
    boat_use_input = forms.FloatField(widget=DualSliderWidget('boat_use_min', 'boat_use_max', min=0, max=100, step=10))

    recfish_use = forms.BooleanField(label="Recreational Fishing Use Intensity", required=False, help_text="Planning units that contain at least one entry for recreational fishing in the 2015 OFR survey", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    recfish_use_min = forms.FloatField(required=False, initial=5, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': ''}))
    recfish_use_max = forms.FloatField(required=False, initial=50, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': 'to'}))
    recfish_use_input = forms.FloatField(widget=DualSliderWidget('recfish_use_min', 'recfish_use_max', min=0, max=100, step=10))

    scuba_use = forms.BooleanField(label="Scuba Diving Use Intensity", required=False, help_text="Planning units that contain at least one entry for SCUBA diving in the 2015 OFR survey", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    scuba_use_min = forms.FloatField(required=False, initial=5, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': ''}))
    scuba_use_max = forms.FloatField(required=False, initial=50, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': 'to'}))
    scuba_use_input = forms.FloatField(widget=DualSliderWidget('scuba_use_min', 'scuba_use_max', min=0, max=100, step=10))

    extdive_use = forms.BooleanField(label="Extractive Diving Use Intensity", required=False, help_text="Planning units that contain at least one entry for extractive diving in the 2015 OFR survey", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    extdive_use_min = forms.FloatField(required=False, initial=5, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': ''}))
    extdive_use_max = forms.FloatField(required=False, initial=50, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': 'to'}))
    extdive_use_input = forms.FloatField(widget=DualSliderWidget('extdive_use_min', 'extdive_use_max', min=0, max=100, step=10))

    spear_use = forms.BooleanField(label="Spearfishing Use Intensity", required=False, help_text="Planning units that contain at least one entry for spearfishing in the 2015 OFR survey", widget=CheckboxInput(attrs={'class': 'parameters hidden_checkbox'}))
    spear_use_min = forms.FloatField(required=False, initial=5, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': ''}))
    spear_use_max = forms.FloatField(required=False, initial=50, widget=forms.TextInput(attrs={'class':'slidervalue', 'pre_text': 'to'}))
    spear_use_input = forms.FloatField(widget=DualSliderWidget('spear_use_min', 'spear_use_max', min=0, max=100, step=10))

    '''
    Depth and Distances
    '''
    def get_step_1_fields(self):
        """Defines the fields that we want to show on the form in step 1, and 
        the order in which they appear, and in groups of 
            (parameter to test, user-min or user-selection, user-max, user-input)
        where each parameter except the first is optional. 
        """
        names = (('depth', 'depth_min', 'depth_max', 'depth_input'),
                ('shore_distance', 'shore_distance_min', 'shore_distance_max', 'shore_distance_input'),
                ('pier_distance', 'pier_distance_min', 'pier_distance_max', 'pier_distance_input'),
                ('inlet_distance', 'inlet_distance_min', None), 
                ('outfall_distance', 'outfall_distance_min', None)) 

        return self._get_fields(names)

    '''
    Some Presence/Absence Stuff
    '''
    def get_step_2_fields(self):
        names = (('injury_site', None, None, 'injury_site_input'),
                ('large_live_coral', None, None, 'large_live_coral_input'), 
                ('pillar_presence', None, None, 'pillar_presence_input'), 
                ('anchorage', None, None, 'anchorage_input'), 
                ('mooring_buoy', None, None, 'mooring_buoy_input'), 
                ('impacted', None, None, 'impacted_input'), 
                ('acropora_pa', None, None, 'acropora_pa_input'))

        return self._get_fields(names)

    '''
    Other Habitats
    '''
    def get_step_3_fields(self):
        names = (('prcnt_sg', 'prcnt_sg_min', 'prcnt_sg_max', 'prcnt_sg_input'),
                ('prcnt_reef', 'prcnt_reef_min', 'prcnt_reef_max', 'prcnt_reef_input'),
                ('prcnt_sand', 'prcnt_sand_min', 'prcnt_sand_max', 'prcnt_sand_input'),
                ('prcnt_art', 'prcnt_art_min', 'prcnt_art_max', 'prcnt_art_input'))

        return self._get_fields(names)

    '''
    More Fish and Coral
    '''
    def get_step_4_fields(self):
        names = (('fish_richness', None, 'fish_richness_max'),
                ('coral_richness', 'coral_richness_min', 'coral_richness_max', 'coral_richness_input'),
                ('coral_density', 'coral_density_min', 'coral_density_max', 'coral_density_input'),
                ('coral_bleach', 'coral_bleach_min', 'coral_bleach_max', 'coral_bleach_input'),
                ('coral_disease', 'coral_disease_min', 'coral_disease_max', 'coral_disease_input'),
                ('coral_resilience', 'coral_resilience_min', 'coral_resilience_max', 'coral_resilience_input'),
                ('reef_fish_density', 'reef_fish_density_min', 'reef_fish_density_max', 'reef_fish_density_input'),
                ('reef_fish_richness', 'reef_fish_richness_min', 'reef_fish_richness_max', 'reef_fish_richness_input'))

        return self._get_fields(names)

    def get_step_5_fields(self):
        names = (('total_use', 'total_use_min', 'total_use_max', 'total_use_input'),
                ('boat_use', 'boat_use_min', 'boat_use_max', 'boat_use_input'),
                ('recfish_use', 'recfish_use_min', 'recfish_use_max', 'recfish_use_input'),
                ('scuba_use', 'scuba_use_min', 'scuba_use_max', 'scuba_use_input'),
                ('extdive_use', 'extdive_use_min', 'extdive_use_max', 'extdive_use_input'),
                ('spear_use', 'spear_use_min', 'spear_use_max', 'spear_use_input'))

        return self._get_fields(names)

    def get_steps(self):
        return self.get_step_1_fields(), \
               self.get_step_2_fields(), \
               self.get_step_3_fields(), \
               self.get_step_4_fields(), \
               self.get_step_5_fields()

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

