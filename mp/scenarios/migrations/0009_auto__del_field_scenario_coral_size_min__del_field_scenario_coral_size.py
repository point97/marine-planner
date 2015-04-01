# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Scenario.coral_size_min'
        db.delete_column(u'scenarios_scenario', 'coral_size_min')

        # Deleting field 'Scenario.coral_size_max'
        db.delete_column(u'scenarios_scenario', 'coral_size_max')

        # Deleting field 'Scenario.coral_size'
        db.delete_column(u'scenarios_scenario', 'coral_size')

        # Adding field 'Scenario.coral_bleach'
        db.add_column(u'scenarios_scenario', 'coral_bleach',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.coral_bleach_min'
        db.add_column(u'scenarios_scenario', 'coral_bleach_min',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.coral_bleach_max'
        db.add_column(u'scenarios_scenario', 'coral_bleach_max',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.coral_disease'
        db.add_column(u'scenarios_scenario', 'coral_disease',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.coral_disease_min'
        db.add_column(u'scenarios_scenario', 'coral_disease_min',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.coral_disease_max'
        db.add_column(u'scenarios_scenario', 'coral_disease_max',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.coral_resilience'
        db.add_column(u'scenarios_scenario', 'coral_resilience',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.coral_resilience_min'
        db.add_column(u'scenarios_scenario', 'coral_resilience_min',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.coral_resilience_max'
        db.add_column(u'scenarios_scenario', 'coral_resilience_max',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.reef_fish_density'
        db.add_column(u'scenarios_scenario', 'reef_fish_density',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.reef_fish_density_min'
        db.add_column(u'scenarios_scenario', 'reef_fish_density_min',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.reef_fish_density_max'
        db.add_column(u'scenarios_scenario', 'reef_fish_density_max',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.reef_fish_richness'
        db.add_column(u'scenarios_scenario', 'reef_fish_richness',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.reef_fish_richness_min'
        db.add_column(u'scenarios_scenario', 'reef_fish_richness_min',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.reef_fish_richness_max'
        db.add_column(u'scenarios_scenario', 'reef_fish_richness_max',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.total_use'
        db.add_column(u'scenarios_scenario', 'total_use',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.total_use_min'
        db.add_column(u'scenarios_scenario', 'total_use_min',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.total_use_max'
        db.add_column(u'scenarios_scenario', 'total_use_max',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.recfish_use'
        db.add_column(u'scenarios_scenario', 'recfish_use',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.recfish_use_min'
        db.add_column(u'scenarios_scenario', 'recfish_use_min',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.recfish_use_max'
        db.add_column(u'scenarios_scenario', 'recfish_use_max',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.scuba_use'
        db.add_column(u'scenarios_scenario', 'scuba_use',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.scuba_use_min'
        db.add_column(u'scenarios_scenario', 'scuba_use_min',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.scuba_use_max'
        db.add_column(u'scenarios_scenario', 'scuba_use_max',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.extdive_use'
        db.add_column(u'scenarios_scenario', 'extdive_use',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.extdive_use_min'
        db.add_column(u'scenarios_scenario', 'extdive_use_min',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.extdive_use_max'
        db.add_column(u'scenarios_scenario', 'extdive_use_max',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.spear_use'
        db.add_column(u'scenarios_scenario', 'spear_use',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.spear_use_min'
        db.add_column(u'scenarios_scenario', 'spear_use_min',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.spear_use_max'
        db.add_column(u'scenarios_scenario', 'spear_use_max',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Adding field 'Scenario.coral_size_min'
        db.add_column(u'scenarios_scenario', 'coral_size_min',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.coral_size_max'
        db.add_column(u'scenarios_scenario', 'coral_size_max',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.coral_size'
        db.add_column(u'scenarios_scenario', 'coral_size',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'Scenario.coral_bleach'
        db.delete_column(u'scenarios_scenario', 'coral_bleach')

        # Deleting field 'Scenario.coral_bleach_min'
        db.delete_column(u'scenarios_scenario', 'coral_bleach_min')

        # Deleting field 'Scenario.coral_bleach_max'
        db.delete_column(u'scenarios_scenario', 'coral_bleach_max')

        # Deleting field 'Scenario.coral_disease'
        db.delete_column(u'scenarios_scenario', 'coral_disease')

        # Deleting field 'Scenario.coral_disease_min'
        db.delete_column(u'scenarios_scenario', 'coral_disease_min')

        # Deleting field 'Scenario.coral_disease_max'
        db.delete_column(u'scenarios_scenario', 'coral_disease_max')

        # Deleting field 'Scenario.coral_resilience'
        db.delete_column(u'scenarios_scenario', 'coral_resilience')

        # Deleting field 'Scenario.coral_resilience_min'
        db.delete_column(u'scenarios_scenario', 'coral_resilience_min')

        # Deleting field 'Scenario.coral_resilience_max'
        db.delete_column(u'scenarios_scenario', 'coral_resilience_max')

        # Deleting field 'Scenario.reef_fish_density'
        db.delete_column(u'scenarios_scenario', 'reef_fish_density')

        # Deleting field 'Scenario.reef_fish_density_min'
        db.delete_column(u'scenarios_scenario', 'reef_fish_density_min')

        # Deleting field 'Scenario.reef_fish_density_max'
        db.delete_column(u'scenarios_scenario', 'reef_fish_density_max')

        # Deleting field 'Scenario.reef_fish_richness'
        db.delete_column(u'scenarios_scenario', 'reef_fish_richness')

        # Deleting field 'Scenario.reef_fish_richness_min'
        db.delete_column(u'scenarios_scenario', 'reef_fish_richness_min')

        # Deleting field 'Scenario.reef_fish_richness_max'
        db.delete_column(u'scenarios_scenario', 'reef_fish_richness_max')

        # Deleting field 'Scenario.total_use'
        db.delete_column(u'scenarios_scenario', 'total_use')

        # Deleting field 'Scenario.total_use_min'
        db.delete_column(u'scenarios_scenario', 'total_use_min')

        # Deleting field 'Scenario.total_use_max'
        db.delete_column(u'scenarios_scenario', 'total_use_max')

        # Deleting field 'Scenario.recfish_use'
        db.delete_column(u'scenarios_scenario', 'recfish_use')

        # Deleting field 'Scenario.recfish_use_min'
        db.delete_column(u'scenarios_scenario', 'recfish_use_min')

        # Deleting field 'Scenario.recfish_use_max'
        db.delete_column(u'scenarios_scenario', 'recfish_use_max')

        # Deleting field 'Scenario.scuba_use'
        db.delete_column(u'scenarios_scenario', 'scuba_use')

        # Deleting field 'Scenario.scuba_use_min'
        db.delete_column(u'scenarios_scenario', 'scuba_use_min')

        # Deleting field 'Scenario.scuba_use_max'
        db.delete_column(u'scenarios_scenario', 'scuba_use_max')

        # Deleting field 'Scenario.extdive_use'
        db.delete_column(u'scenarios_scenario', 'extdive_use')

        # Deleting field 'Scenario.extdive_use_min'
        db.delete_column(u'scenarios_scenario', 'extdive_use_min')

        # Deleting field 'Scenario.extdive_use_max'
        db.delete_column(u'scenarios_scenario', 'extdive_use_max')

        # Deleting field 'Scenario.spear_use'
        db.delete_column(u'scenarios_scenario', 'spear_use')

        # Deleting field 'Scenario.spear_use_min'
        db.delete_column(u'scenarios_scenario', 'spear_use_min')

        # Deleting field 'Scenario.spear_use_max'
        db.delete_column(u'scenarios_scenario', 'spear_use_max')



    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'scenarios.gridcell': {
            'Meta': {'object_name': 'GridCell'},
            'acerv_area': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'acropora_pa': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'anchor_density': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'anchor_desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'anchorage': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'art_area': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'centroid': ('django.contrib.gis.db.models.fields.PointField', [], {'srid': '3857', 'null': 'True', 'blank': 'True'}),
            'coral_bleach': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'coral_cover': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'coral_density': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'coral_disease': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'coral_resilience': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'coral_richness': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'county': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'depth_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'depth_mean': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'depth_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'esa_spp': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'extdive_use': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fish_density': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fish_div': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fish_richness': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '3857', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impacted': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'injury_site': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'inlet_distance': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'large_live_coral': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'lionfish': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'major_habitat': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'mooring_buoy': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'mooring_density': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mooring_desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'outfall_distance': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'pier_distance': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'pillar_presence': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'prcnt_art': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'prcnt_reef': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'prcnt_sand': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'prcnt_sg': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'recfish_use': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'reef_area': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'reef_fish_density': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'reef_fish_richness': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sand_area': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'scuba_use': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sg_area': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'shore_distance': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'spear_use': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'total_use': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'unique_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'scenarios.scenario': {
            'Meta': {'object_name': 'Scenario'},
            'acropora_pa': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'acropora_pa_input': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'anchorage': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'anchorage_input': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'scenarios_scenario_related'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'coral_bleach': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'coral_bleach_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'coral_bleach_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'coral_density': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'coral_density_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'coral_density_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'coral_disease': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'coral_disease_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'coral_disease_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'coral_resilience': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'coral_resilience_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'coral_resilience_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'coral_richness': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'coral_richness_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'coral_richness_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'depth': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'depth_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'depth_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'extdive_use': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'extdive_use_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'extdive_use_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'fish_richness': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fish_richness_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'fish_richness_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'geometry_dissolved': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '3857', 'null': 'True', 'blank': 'True'}),
            'geometry_final_area': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'grid_cells': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impacted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'impacted_input': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'injury_site': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'injury_site_input': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'inlet_distance': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'inlet_distance_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'inlet_distance_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'large_live_coral': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'large_live_coral_input': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'mooring_buoy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mooring_buoy_input': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': "'255'"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'outfall_distance': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'outfall_distance_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'outfall_distance_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'pier_distance': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pier_distance_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'pier_distance_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'pillar_presence': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pillar_presence_input': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'prcnt_art': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'prcnt_art_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'prcnt_art_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'prcnt_reef': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'prcnt_reef_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'prcnt_reef_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'prcnt_sand': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'prcnt_sand_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'prcnt_sand_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'prcnt_sg': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'prcnt_sg_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'prcnt_sg_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'recfish_use': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'recfish_use_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'recfish_use_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'reef_fish_density': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reef_fish_density_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'reef_fish_density_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'reef_fish_richness': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reef_fish_richness_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'reef_fish_richness_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'satisfied': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'scuba_use': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'scuba_use_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'scuba_use_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sharing_groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'scenarios_scenario_related'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.Group']"}),
            'shore_distance': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shore_distance_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'shore_distance_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'spear_use': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'spear_use_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'spear_use_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'total_use': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'total_use_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'total_use_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'scenarios_scenario_related'", 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['scenarios']