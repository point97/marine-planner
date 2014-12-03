# coding: utf-8

import os
import time
import json
from picklefield import PickledObjectField
from django.conf import settings
from django.contrib.gis.db import models
from django.utils.html import escape
from madrona.common.utils import asKml
from madrona.common.jsonutils import get_properties_json, get_feature_json
from madrona.features import register
from madrona.analysistools.models import Analysis
from general.utils import miles_to_meters, feet_to_meters, meters_to_feet, mph_to_mps, mps_to_mph, format
from django.contrib.gis.geos import MultiPolygon
from django.contrib.gis.db.models.aggregates import Union


class KMLCache(models.Model):
    key = models.CharField(max_length=150) 
    val = PickledObjectField()
    date_modified = models.DateTimeField(auto_now=True)   
    
@register
class Scenario(Analysis):
    bathy_avg = models.BooleanField()
    bathy_avg_min = models.FloatField(null=True, blank=True)
    bathy_avg_max = models.FloatField(null=True, blank=True)

    wind_avg = models.BooleanField()
    wind_avg_min = models.FloatField(null=True, blank=True)
    wind_avg_max = models.FloatField(null=True, blank=True)

    subs_mind = models.BooleanField()
    subs_mind_min = models.FloatField(null=True, blank=True)
    subs_mind_max = models.FloatField(null=True, blank=True)

    coast_avg = models.BooleanField()
    coast_avg_min = models.FloatField(null=True, blank=True)
    coast_avg_max = models.FloatField(null=True, blank=True)

    mangrove_p = models.BooleanField()
    mangrove_p_min = models.FloatField(null=True, blank=True)
    mangrove_p_max = models.FloatField(null=True, blank=True)
    
    coral_p = models.BooleanField()
    coral_p_min = models.FloatField(null=True, blank=True)
    coral_p_max = models.FloatField(null=True, blank=True)

    subveg_p = models.BooleanField()
    subveg_p_max = models.FloatField(null=True, blank=True)
    subveg_p_min = models.FloatField(null=True, blank=True)

    protarea_p = models.BooleanField()
    protarea_p_min = models.FloatField(null=True, blank=True)
    protarea_p_max = models.FloatField(null=True, blank=True)

    pr_apc_p = models.BooleanField()
    pr_apc_p_min = models.FloatField(null=True, blank=True)
    pr_apc_p_max = models.FloatField(null=True, blank=True)

    pr_ape_p = models.BooleanField()
    pr_ape_p_min = models.FloatField(null=True, blank=True)
    pr_ape_p_max = models.FloatField(null=True, blank=True)

    vi_apc_p = models.BooleanField()
    vi_apc_p_min = models.FloatField(null=True, blank=True)
    vi_apc_p_max = models.FloatField(null=True, blank=True)

    
    description = models.TextField(null=True, blank=True)
    satisfied = models.BooleanField(default=True, help_text="Am I satisfied?")
    active = models.BooleanField(default=True)
            
    lease_blocks = models.TextField(verbose_name='Lease Block IDs', null=True, 
                                    blank=True)
    geometry_final_area = models.FloatField(verbose_name='Total Area', 
                                            null=True, blank=True)
    geometry_dissolved = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, 
                                                  null=True, blank=True, 
                                                  verbose_name="Scenario result dissolved")
                
    @property
    def serialize_attributes(self):
        """Return attributes in text format. Used to display information on
        click in the planner. 
        """
        from general.utils import format
        attributes = []

        if self.bathy_avg:
            attributes.append(dict(title='Depth Range', 
                                   data='%s - %s meters' % (self.bathy_avg_min, 
                                                            self.bathy_avg_max)))
        
        if self.wind_avg:
            attributes.append(dict(title='Minimum Wind Potential', 
                                   data='%s W/m²' % (self.wind_avg_min)))
         
        if self.subs_mind:
            attributes.append(dict(title='Maximum Distance to Substation', 
                                   data='%s meters' % (self.subs_mind_max)))
         
        if self.coast_avg:
            attributes.append(dict(title='Distance to Shore', 
                                   data='%s - %s meters' % (self.coast_avg_min, 
                                                            self.coast_avg_max)))

        if self.mangrove_p or self.coral_p or self.subveg_p or self.protarea_p or self.pr_apc_p or self.pr_ape_p or self.vi_apc_p:
            exclusions = ''
            if self.mangrove_p:
                exclusions += '<br>&nbsp;&nbsp; Mangroves'
            if self.coral_p:
                exclusions += '<br>&nbsp;&nbsp; Corals'
            if self.subveg_p:
                exclusions += '<br>&nbsp;&nbsp; Submerged Vegetation'
            if self.protarea_p:
                exclusions += '<br>&nbsp;&nbsp; Protected Areas'
            if self.pr_apc_p:
                exclusions += '<br>&nbsp;&nbsp; Puerto Rico Conservation Priority Areas'
            if self.pr_ape_p:
                exclusions += '<br>&nbsp;&nbsp; Puerto Rico Special Planning Areas'
            if self.vi_apc_p:
                exclusions += '<br>&nbsp;&nbsp; USVI Areas of Particular Concern'

            attributes.append(dict(title='Grid cells containing the following were excluded', data=exclusions))

        # if self.mangrove_p:
        #     attributes.append(dict(title='Mangroves', 
        #                            data='%s - %s %%' % (self.mangrove_p_min, 
        #                                                 self.mangrove_p_max)))

        # if self.coral_p:
        #     attributes.append(dict(title='Coral', 
        #                            data='%s - %s %%' % (self.coral_p_min, 
        #                                                 self.coral_p_max)))

        # if self.subveg_p:
        #     attributes.append(dict(title='Subveg', 
        #                            data='%s - %s %%' % (self.subveg_p_min, 
        #                                                 self.subveg_p_max)))

        # if self.protarea_p:
        #     attributes.append(dict(title='protarea', 
        #                            data='%s - %s %%' % (self.protarea_p_min, 
        #                                                 self.protarea_p_max)))

        # if self.pr_apc_p:
        #     attributes.append(dict(title='pr_apc_p', 
        #                            data='%s - %s %%' % (self.pr_apc_p_min, 
        #                                                 self.pr_apc_p_max)))

        # if self.pr_ape_p:
        #     attributes.append(dict(title='pr_ape_p', 
        #                            data='%s - %s %%' % (self.pr_ape_p_min, 
        #                                                 self.pr_ape_p_max)))

        # if self.vi_apc_p:
        #     attributes.append(dict(title='USVI Areas of Particular Concern', 
        #                            data='%s - %s %%' % (self.vi_apc_p_min, 
        #                                                 self.vi_apc_p_max)))

        attributes.append({'title': 'Number of Leaseblocks', 
                           'data': self.lease_blocks.count(',')+1})
        return { 'event': 'click', 'attributes': attributes }
    
    
    def geojson(self, srid):
        props = get_properties_json(self)
        props['absolute_url'] = self.get_absolute_url()
        json_geom = self.geometry_dissolved.transform(srid, clone=True).json
        return get_feature_json(json_geom, json.dumps(props))
    
    def run(self):
        query = LeaseBlock.objects.all()
        
        # TODO: This would be nicer if it generically knew how to filter fields
        # by name, and what kinds of filters they were. For now, hard code. 
        
        if self.bathy_avg:
            query = query.filter(bathy_avg__range=(self.bathy_avg_min, 
                                                   self.bathy_avg_max))
        
        if self.wind_avg:
            query = query.filter(wind_avg__gt=self.wind_avg_min)
        
        if self.subs_mind:
            query = query.filter(subs_mind__lt=self.subs_mind_max)
        
        if self.coast_avg:
            query = query.filter(coast_avg__range=(self.coast_avg_min, 
                                                   self.coast_avg_max))
        
        if self.mangrove_p:
            query = query.filter(mangrove_p=0)
        
        if self.coral_p:
            query = query.filter(coral_p=0)
        
        if self.subveg_p:
            query = query.filter(subveg_p=0)
        
        if self.protarea_p:
            query = query.filter(protarea_p=0)
        
        if self.pr_apc_p:
            query = query.filter(pr_apc_p=0)
        
        if self.pr_ape_p:
            query = query.filter(pr_ape_p=0)
        
        if self.vi_apc_p:
            query = query.filter(vi_apc_p=0)
        
        dissolved_geom = query.aggregate(Union('geometry'))
        if dissolved_geom:
            dissolved_geom = dissolved_geom['geometry__union']
        else:
            raise Exception("No lease blocks available with the current filters.")
        
        if type(dissolved_geom) == MultiPolygon:
            self.geometry_dissolved = dissolved_geom
        else:
            self.geometry_dissolved = MultiPolygon(dissolved_geom, srid=dissolved_geom.srid)
        self.active = True
        
        import datetime;start=datetime.datetime.now()
        self.geometry_final_area = self.geometry_dissolved.area
        
        self.lease_blocks = ','.join(str(i) 
                                     for i in query.values_list('id', flat=True))
        
        print("Elapsed:", datetime.datetime.now() - start)
               
        if self.lease_blocks == '':
            self.satisfied = False
        else:
            self.satisfied = True
        return True        
    
    def save(self, rerun=None, *args, **kwargs):
        if rerun is None and self.pk is None:
            rerun = True
        if rerun is None and self.pk is not None: #if editing a scenario and no value for rerun is given
            rerun = False
            if not rerun:
                orig = Scenario.objects.get(pk=self.pk)
                #TODO: keeping this in here til I figure out why self.lease_blocks and self.geometry_final_area are emptied when run() is not called
                rerun = True
                #if getattr(orig, 'name') != getattr(self, 'name'):
                #    #print 'name has changed'
                #    remove_kml_cache(self) 
                #    rerun = True
                if not rerun:
                    for f in Scenario.input_fields():
                        # Is original value different from form value?
                        if getattr(orig, f.name) != getattr(self, f.name):
                            #print 'input_field, %s, has changed' %f.name
                            rerun = True
                            break                                                                                                                   
                if not rerun:
                    '''
                        the substrates need to be grabbed, then saved, then grabbed again because 
                        both getattr calls (orig and self) return the same original list until the model has been saved 
                        (perhaps because form.save_m2m has to be called), after which calls to getattr will 
                        return the same list (regardless of whether we use orig or self)
                    ''' 
                    orig_weas = set(getattr(self, 'input_wea').all())   
                    orig_substrates = set(getattr(self, 'input_substrate').all())  
                    orig_sediments = set(getattr(self, 'input_sediment').all())                    
                    super(Scenario, self).save(rerun=False, *args, **kwargs)  
                    new_weas = set(getattr(self, 'input_wea').all())                   
                    new_substrates = set(getattr(self, 'input_substrate').all()) 
                    new_sediments = set(getattr(self, 'input_sediment').all())   
                    if orig_substrates != new_substrates or orig_sediments != new_sediments or orig_weas != new_weas:
                        rerun = True    
            super(Scenario, self).save(rerun=rerun, *args, **kwargs)
        else: #editing a scenario and rerun is provided 
            super(Scenario, self).save(rerun=rerun, *args, **kwargs)
    
    def delete(self, *args, **kwargs):
        """
        Remove KML cache before removing scenario 
        """
        from kml_caching import remove_kml_cache
        remove_kml_cache(self)
        super(Scenario, self).delete(*args, **kwargs)    
    
    def __unicode__(self):
        return u'%s' % self.name
        
    def support_filename(self):
        return os.path.basename(self.support_file.name)
        
    @classmethod
    def mapnik_geomfield(self):
        return "output_geom"

    @classmethod
    def mapnik_style(self):
        import mapnik
        polygon_style = mapnik.Style()
        
        ps = mapnik.PolygonSymbolizer(mapnik.Color('#ffffff'))
        ps.fill_opacity = 0.5
        
        ls = mapnik.LineSymbolizer(mapnik.Color('#555555'),0.75)
        ls.stroke_opacity = 0.5
        
        r = mapnik.Rule()
        r.symbols.append(ps)
        r.symbols.append(ls)
        polygon_style.rules.append(r)
        return polygon_style     
    
    @classmethod
    def input_parameter_fields(klass):
        return [f for f in klass._meta.fields if f.attname.startswith('input_parameter_')]

    @classmethod
    def input_filter_fields(klass):
        return [f for f in klass._meta.fields if f.attname.startswith('input_filter_')]

    @property
    def lease_blocks_set(self):
        if len(self.lease_blocks) == 0:  #empty result
            leaseblock_ids = []
        else:
            leaseblock_ids = [int(id) for id in self.lease_blocks.split(',')]
        leaseblocks = LeaseBlock.objects.filter(pk__in=leaseblock_ids)
        return leaseblocks
    
    @property
    def num_lease_blocks(self):
        if self.lease_blocks == '':
            return 0
        return len(self.lease_blocks.split(','))
    
    @property
    def geometry_is_empty(self):
        return len(self.lease_blocks) == 0
    
    @property
    def input_wea_names(self):
        return [wea.wea_name for wea in self.input_wea.all()]
        
    @property
    def input_substrate_names(self):
        return [substrate.substrate_name for substrate in self.input_substrate.all()]
        
    @property
    def input_sediment_names(self):
        return [sediment.sediment_name for sediment in self.input_sediment.all()]
    
    #TODO: is this being used...?  Yes, see show.html
    @property
    def has_wind_energy_criteria(self):
        wind_parameters = Scenario.input_parameter_fields()
        for wp in wind_parameters:
            if getattr(self, wp.name):
                return True
        return False
        
    @property
    def has_shipping_filters(self):
        shipping_filters = Scenario.input_filter_fields()
        for sf in shipping_filters:
            if getattr(self, sf.name):
                return True
        return False 
        
    @property
    def has_military_filters(self):
        return False
    
    @property
    def color(self):
        try:
            return Objective.objects.get(pk=self.input_objectives.values_list()[0][0]).color
        except:
            return '778B1A55'

    @property 
    def kml_working(self):
        return """
        <Placemark id="%s">
            <visibility>0</visibility>
            <name>%s (WORKING)</name>
        </Placemark>
        """ % (self.uid, escape(self.name))

    @property 
    def kml(self):  
        #from general.utils import format 
        import time

        #the following list appendation strategy was a good 10% faster than string concatenation
        #(biggest improvement however came by adding/populating a geometry_client column in leaseblock table)
        combined_kml_list = []
        if len(self.lease_blocks) == 0:  #empty result
            leaseblock_ids = []
            combined_kml_list.append('<Folder id="%s"><name>%s -- 0 Leaseblocks</name><visibility>0</visibility><open>0</open>' %(self.uid, self.name))
        else:
            leaseblock_ids = [int(id) for id in self.lease_blocks.split(',')]
            combined_kml_list.append('<Folder id="%s"><name>%s</name><visibility>0</visibility><open>0</open>' %(self.uid, self.name))
        combined_kml_list.append('<LookAt><longitude>-73.5</longitude><latitude>39</latitude><heading>0</heading><range>600000</range></LookAt>')
        combined_kml_list.append('<styleUrl>#%s-default</styleUrl>' % (self.model_uid()))
        combined_kml_list.append('%s' % self.leaseblock_style())
        print 'Generating KML for %s Lease Blocks' % len(leaseblock_ids)
        start_time = time.time()
        leaseblocks = LeaseBlock.objects.filter(pk__in=leaseblock_ids)
        for leaseblock in leaseblocks:
            try:
                kml =   """
                    <Placemark>
                        <visibility>1</visibility>
                        <styleUrl>#%s-leaseblock</styleUrl>
                        <ExtendedData>
                            <Data name="header"><value>%s</value></Data>
                            <Data name="prot_number"><value>%s</value></Data>
                            <Data name="depth_range_output"><value>%s</value></Data>
                            <Data name="substrate"><value>%s</value></Data>
                            <Data name="sediment"><value>%s</value></Data>
                            <Data name="wea_label"><value>%s</value></Data>
                            <Data name="wea_state_name"><value>%s</value></Data>
                            <Data name="distance_to_shore"><value>%s</value></Data>
                            <Data name="distance_to_awc"><value>%s</value></Data>
                            <Data name="wind_speed_output"><value>%s</value></Data>
                            <Data name="ais_density"><value>%s</value></Data>
                            <Data name="user"><value>%s</value></Data>
                            <Data name="modified"><value>%s</value></Data>
                        </ExtendedData>
                        %s
                    </Placemark>
                    """ % ( self.model_uid(), self.name, leaseblock.prot_numb,                             
                            leaseblock.depth_range_output, 
                            leaseblock.majority_seabed, #LeaseBlock Update: might change back to leaseblock.substrate
                            leaseblock.majority_sediment, #TODO: might change sediment to a more user friendly output
                            leaseblock.wea_label,
                            leaseblock.wea_state_name,
                            format(leaseblock.avg_distance,0), format(leaseblock.awc_min_distance,0),
                            #LeaseBlock Update: added the following two entries (min and max) to replace avg wind speed for now
                            leaseblock.wind_speed_output,
                            leaseblock.ais_density,
                            self.user, self.date_modified.replace(microsecond=0), 
                            #asKml(leaseblock.geometry.transform( settings.GEOMETRY_CLIENT_SRID, clone=True ))
                            asKml(leaseblock.geometry_client)
                          ) 
            except: 
                #this is in place to handle (at least one - "NJ18-05_6420") instance in which null value was used in float field max_distance
                print "The following leaseblock threw an error while generating KML:  %s" %leaseblock.prot_numb
                continue
            combined_kml_list.append(kml )
        combined_kml_list.append("</Folder>")
        combined_kml = ''.join(combined_kml_list)
        elapsed_time = time.time() - start_time
        print 'Finished generating KML (with a list) for %s Lease Blocks in %s seconds' % (len(leaseblock_ids), elapsed_time)
        
        return combined_kml
    
    def leaseblock_style(self):
        #LeaseBlock Update:  changed the following from <p>Avg Wind Speed: $[wind_speed] 
        return  """
                <Style id="%s-leaseblock">
                    <BalloonStyle>
                        <bgColor>ffeeeeee</bgColor>
                        <text> <![CDATA[
                            <font color="#1A3752">
                                Spatial Design for Wind Energy: <strong>$[header]</strong>
                                <p>
                                <table width="250">
                                    <tr><td> Lease Block Number: <b>$[prot_number]</b> </td></tr>
                                </table>
                                <table width="250">
                                    <tr><td> $[wea_label] <b>$[wea_state_name]</b> </td></tr>
                                    <tr><td> Avg Wind Speed: <b>$[wind_speed_output]</b> </td></tr>
                                    <tr><td> Distance to AWC Station: <b>$[distance_to_awc] miles</b> </td></tr>
                                </table>
                                <table width="250">
                                    <tr><td> Distance to Shore: <b>$[distance_to_shore] miles</b> </td></tr>
                                    <tr><td> Depth: <b>$[depth_range_output]</b> </td></tr>
                                    <tr><td> Majority Seabed Form: <b>$[substrate]</b> </td></tr>
                                    <tr><td> Majority Sediment: <b>$[sediment]</b> </td></tr>
                                </table>
                                <table width="250">
                                    <tr><td> Shipping Density: <b>$[ais_density]</b> </td></tr>
                                </table>
                            </font>  
                            <font size=1>created by $[user] on $[modified]</font>
                        ]]> </text>
                    </BalloonStyle>
                    <LineStyle>
                        <color>ff8B1A55</color>
                    </LineStyle>
                    <PolyStyle>
                        <color>778B1A55</color>
                    </PolyStyle>
                </Style>
            """ % (self.model_uid())
        
    @property
    def kml_style(self):
        return """
        <Style id="%s-default">
            <ListStyle>
                <listItemType>checkHideChildren</listItemType>
            </ListStyle>
        </Style>
        """ % (self.model_uid())
        
    @property
    def get_id(self):
        return self.id
    
    class Options:
        verbose_name = 'Spatial Design for Wind Energy'
        icon_url = 'marco/img/multi.png'
        form = 'scenarios.forms.ScenarioForm'
        form_template = 'scenario/form.html'
        show_template = 'scenario/show.html'

#no longer needed?
class Objective(models.Model):
    name = models.CharField(max_length=35)
    color = models.CharField(max_length=8, default='778B1A55')
    
    def __unicode__(self):
        return u'%s' % self.name        

#no longer needed?
class Parameter(models.Model):
    ordering_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=35, null=True, blank=True)
    shortname = models.CharField(max_length=35, null=True, blank=True)
    objectives = models.ManyToManyField("Objective", null=True, blank=True)
    
    def __unicode__(self):
        return u'%s' % self.name

class LeaseBlock(models.Model):
    wind_min = models.FloatField(help_text="Units are Wind Units")
    wind_max = models.FloatField()
    wind_avg = models.FloatField()
    bathy_min = models.IntegerField()
    bathy_max = models.IntegerField()
    bathy_avg = models.FloatField()
    mangrove_p = models.FloatField()
    coral_p = models.FloatField()
    subveg_p = models.FloatField()
    protarea_p = models.FloatField()
    subs_minid = models.IntegerField()
    subs_mind = models.FloatField()
    subs_avgid = models.IntegerField()
    subs_avgd = models.FloatField()
    coast_min = models.FloatField()
    coast_avg = models.FloatField()
    pr_apc_p = models.FloatField()
    pr_ape_p = models.FloatField()
    vi_apc_p = models.FloatField()
    objects = models.GeoManager()

    geometry = models.MultiPolygonField(srid=settings.GEOMETRY_DB_SRID, 
                                    null=True, blank=True, 
                                    verbose_name="Lease Block Geometry")
    objects = models.GeoManager()   

    @property
    def wind_speed_output(self):
        if self.wind_min == self.wind_max:
            return "%s mph?" %format(mps_to_mph(self.wind_min),1)
        else:
            return "%s - %s mph?" %( format(mps_to_mph(self.wind_min),1), format(mps_to_mph(self.wind_max),1) )

    @property
    def depth_range_output(self):
        if self.bathy_min == self.bathy_max:
            return "%s meters?" %format(-self.bathy_min,0)
        else:
            return "%s - %s meters?" %( format(-self.bathy_min,0), format(-self.bathy_max,0) )     
        
    @property 
    def kml_done(self):
        return """
        <Placemark id="%s">
            <visibility>1</visibility>
            <styleUrl>#%s-default</styleUrl>
            %s
        </Placemark>
        """ % ( self.uid, self.model_uid(),
                asKml(self.geometry.transform( settings.GEOMETRY_CLIENT_SRID, clone=True ))
              )        
