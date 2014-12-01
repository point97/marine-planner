# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Scenario.input_parameter_distance_to_shore'
        db.delete_column('scenarios_scenario', 'input_parameter_distance_to_shore')

        # Deleting field 'Scenario.input_parameter_wind_speed'
        db.delete_column('scenarios_scenario', 'input_parameter_wind_speed')

        # Deleting field 'Scenario.input_parameter_depth'
        db.delete_column('scenarios_scenario', 'input_parameter_depth')

        # Deleting field 'Scenario.input_max_distance_to_shore'
        db.delete_column('scenarios_scenario', 'input_max_distance_to_shore')

        # Deleting field 'Scenario.input_min_depth'
        db.delete_column('scenarios_scenario', 'input_min_depth')

        # Deleting field 'Scenario.input_avg_wind_speed'
        db.delete_column('scenarios_scenario', 'input_avg_wind_speed')

        # Deleting field 'Scenario.input_filter_uxo'
        db.delete_column('scenarios_scenario', 'input_filter_uxo')

        # Deleting field 'Scenario.input_min_distance_to_shore'
        db.delete_column('scenarios_scenario', 'input_min_distance_to_shore')

        # Deleting field 'Scenario.input_max_depth'
        db.delete_column('scenarios_scenario', 'input_max_depth')

        # Adding field 'Scenario.bathy_avg'
        db.add_column('scenarios_scenario', 'bathy_avg',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.bathy_avg_min'
        db.add_column('scenarios_scenario', 'bathy_avg_min',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.bathy_avg_max'
        db.add_column('scenarios_scenario', 'bathy_avg_max',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.wind_avg'
        db.add_column('scenarios_scenario', 'wind_avg',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.wind_avg_min'
        db.add_column('scenarios_scenario', 'wind_avg_min',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.wind_avg_max'
        db.add_column('scenarios_scenario', 'wind_avg_max',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.subs_mind'
        db.add_column('scenarios_scenario', 'subs_mind',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.subs_mind_min'
        db.add_column('scenarios_scenario', 'subs_mind_min',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.subs_mind_max'
        db.add_column('scenarios_scenario', 'subs_mind_max',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.coast_avg'
        db.add_column('scenarios_scenario', 'coast_avg',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.coast_avg_min'
        db.add_column('scenarios_scenario', 'coast_avg_min',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.coast_avg_max'
        db.add_column('scenarios_scenario', 'coast_avg_max',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.mangrove_p'
        db.add_column('scenarios_scenario', 'mangrove_p',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.mangrove_p_min'
        db.add_column('scenarios_scenario', 'mangrove_p_min',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.mangrove_p_max'
        db.add_column('scenarios_scenario', 'mangrove_p_max',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.coral_p'
        db.add_column('scenarios_scenario', 'coral_p',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.coral_p_min'
        db.add_column('scenarios_scenario', 'coral_p_min',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.coral_p_max'
        db.add_column('scenarios_scenario', 'coral_p_max',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.subveg_p'
        db.add_column('scenarios_scenario', 'subveg_p',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.subveg_p_max'
        db.add_column('scenarios_scenario', 'subveg_p_max',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.subveg_p_min'
        db.add_column('scenarios_scenario', 'subveg_p_min',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.protarea_p'
        db.add_column('scenarios_scenario', 'protarea_p',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.protarea_p_min'
        db.add_column('scenarios_scenario', 'protarea_p_min',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.protarea_p_max'
        db.add_column('scenarios_scenario', 'protarea_p_max',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.pr_apc_p'
        db.add_column('scenarios_scenario', 'pr_apc_p',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.pr_apc_p_min'
        db.add_column('scenarios_scenario', 'pr_apc_p_min',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.pr_apc_p_max'
        db.add_column('scenarios_scenario', 'pr_apc_p_max',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.pr_ape_p'
        db.add_column('scenarios_scenario', 'pr_ape_p',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.pr_ape_p_min'
        db.add_column('scenarios_scenario', 'pr_ape_p_min',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.pr_ape_p_max'
        db.add_column('scenarios_scenario', 'pr_ape_p_max',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.vi_apc_p'
        db.add_column('scenarios_scenario', 'vi_apc_p',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.vi_apc_p_min'
        db.add_column('scenarios_scenario', 'vi_apc_p_min',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.vi_apc_p_max'
        db.add_column('scenarios_scenario', 'vi_apc_p_max',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Scenario.input_parameter_distance_to_shore'
        db.add_column('scenarios_scenario', 'input_parameter_distance_to_shore',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.input_parameter_wind_speed'
        db.add_column('scenarios_scenario', 'input_parameter_wind_speed',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.input_parameter_depth'
        db.add_column('scenarios_scenario', 'input_parameter_depth',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.input_max_distance_to_shore'
        db.add_column('scenarios_scenario', 'input_max_distance_to_shore',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.input_min_depth'
        db.add_column('scenarios_scenario', 'input_min_depth',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.input_avg_wind_speed'
        db.add_column('scenarios_scenario', 'input_avg_wind_speed',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.input_filter_uxo'
        db.add_column('scenarios_scenario', 'input_filter_uxo',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Scenario.input_min_distance_to_shore'
        db.add_column('scenarios_scenario', 'input_min_distance_to_shore',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Scenario.input_max_depth'
        db.add_column('scenarios_scenario', 'input_max_depth',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Scenario.bathy_avg'
        db.delete_column('scenarios_scenario', 'bathy_avg')

        # Deleting field 'Scenario.bathy_avg_min'
        db.delete_column('scenarios_scenario', 'bathy_avg_min')

        # Deleting field 'Scenario.bathy_avg_max'
        db.delete_column('scenarios_scenario', 'bathy_avg_max')

        # Deleting field 'Scenario.wind_avg'
        db.delete_column('scenarios_scenario', 'wind_avg')

        # Deleting field 'Scenario.wind_avg_min'
        db.delete_column('scenarios_scenario', 'wind_avg_min')

        # Deleting field 'Scenario.wind_avg_max'
        db.delete_column('scenarios_scenario', 'wind_avg_max')

        # Deleting field 'Scenario.subs_mind'
        db.delete_column('scenarios_scenario', 'subs_mind')

        # Deleting field 'Scenario.subs_mind_min'
        db.delete_column('scenarios_scenario', 'subs_mind_min')

        # Deleting field 'Scenario.subs_mind_max'
        db.delete_column('scenarios_scenario', 'subs_mind_max')

        # Deleting field 'Scenario.coast_avg'
        db.delete_column('scenarios_scenario', 'coast_avg')

        # Deleting field 'Scenario.coast_avg_min'
        db.delete_column('scenarios_scenario', 'coast_avg_min')

        # Deleting field 'Scenario.coast_avg_max'
        db.delete_column('scenarios_scenario', 'coast_avg_max')

        # Deleting field 'Scenario.mangrove_p'
        db.delete_column('scenarios_scenario', 'mangrove_p')

        # Deleting field 'Scenario.mangrove_p_min'
        db.delete_column('scenarios_scenario', 'mangrove_p_min')

        # Deleting field 'Scenario.mangrove_p_max'
        db.delete_column('scenarios_scenario', 'mangrove_p_max')

        # Deleting field 'Scenario.coral_p'
        db.delete_column('scenarios_scenario', 'coral_p')

        # Deleting field 'Scenario.coral_p_min'
        db.delete_column('scenarios_scenario', 'coral_p_min')

        # Deleting field 'Scenario.coral_p_max'
        db.delete_column('scenarios_scenario', 'coral_p_max')

        # Deleting field 'Scenario.subveg_p'
        db.delete_column('scenarios_scenario', 'subveg_p')

        # Deleting field 'Scenario.subveg_p_max'
        db.delete_column('scenarios_scenario', 'subveg_p_max')

        # Deleting field 'Scenario.subveg_p_min'
        db.delete_column('scenarios_scenario', 'subveg_p_min')

        # Deleting field 'Scenario.protarea_p'
        db.delete_column('scenarios_scenario', 'protarea_p')

        # Deleting field 'Scenario.protarea_p_min'
        db.delete_column('scenarios_scenario', 'protarea_p_min')

        # Deleting field 'Scenario.protarea_p_max'
        db.delete_column('scenarios_scenario', 'protarea_p_max')

        # Deleting field 'Scenario.pr_apc_p'
        db.delete_column('scenarios_scenario', 'pr_apc_p')

        # Deleting field 'Scenario.pr_apc_p_min'
        db.delete_column('scenarios_scenario', 'pr_apc_p_min')

        # Deleting field 'Scenario.pr_apc_p_max'
        db.delete_column('scenarios_scenario', 'pr_apc_p_max')

        # Deleting field 'Scenario.pr_ape_p'
        db.delete_column('scenarios_scenario', 'pr_ape_p')

        # Deleting field 'Scenario.pr_ape_p_min'
        db.delete_column('scenarios_scenario', 'pr_ape_p_min')

        # Deleting field 'Scenario.pr_ape_p_max'
        db.delete_column('scenarios_scenario', 'pr_ape_p_max')

        # Deleting field 'Scenario.vi_apc_p'
        db.delete_column('scenarios_scenario', 'vi_apc_p')

        # Deleting field 'Scenario.vi_apc_p_min'
        db.delete_column('scenarios_scenario', 'vi_apc_p_min')

        # Deleting field 'Scenario.vi_apc_p_max'
        db.delete_column('scenarios_scenario', 'vi_apc_p_max')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'scenarios.kmlcache': {
            'Meta': {'object_name': 'KMLCache'},
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'val': ('picklefield.fields.PickledObjectField', [], {})
        },
        'scenarios.leaseblock': {
            'Meta': {'object_name': 'LeaseBlock'},
            'bathy_avg': ('django.db.models.fields.FloatField', [], {}),
            'bathy_max': ('django.db.models.fields.IntegerField', [], {}),
            'bathy_min': ('django.db.models.fields.IntegerField', [], {}),
            'coast_avg': ('django.db.models.fields.FloatField', [], {}),
            'coast_min': ('django.db.models.fields.FloatField', [], {}),
            'coral_p': ('django.db.models.fields.FloatField', [], {}),
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '3857', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mangrove_p': ('django.db.models.fields.FloatField', [], {}),
            'pr_apc_p': ('django.db.models.fields.FloatField', [], {}),
            'pr_ape_p': ('django.db.models.fields.FloatField', [], {}),
            'protarea_p': ('django.db.models.fields.FloatField', [], {}),
            'subs_avgd': ('django.db.models.fields.FloatField', [], {}),
            'subs_avgid': ('django.db.models.fields.IntegerField', [], {}),
            'subs_mind': ('django.db.models.fields.FloatField', [], {}),
            'subs_minid': ('django.db.models.fields.IntegerField', [], {}),
            'subveg_p': ('django.db.models.fields.FloatField', [], {}),
            'vi_apc_p': ('django.db.models.fields.FloatField', [], {}),
            'wind_avg': ('django.db.models.fields.FloatField', [], {}),
            'wind_max': ('django.db.models.fields.FloatField', [], {}),
            'wind_min': ('django.db.models.fields.FloatField', [], {})
        },
        'scenarios.objective': {
            'Meta': {'object_name': 'Objective'},
            'color': ('django.db.models.fields.CharField', [], {'default': "'778B1A55'", 'max_length': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '35'})
        },
        'scenarios.parameter': {
            'Meta': {'object_name': 'Parameter'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'objectives': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['scenarios.Objective']", 'null': 'True', 'blank': 'True'}),
            'ordering_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'shortname': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'})
        },
        'scenarios.scenario': {
            'Meta': {'object_name': 'Scenario'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'bathy_avg': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'bathy_avg_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'bathy_avg_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'coast_avg': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'coast_avg_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'coast_avg_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'scenarios_scenario_related'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'coral_p': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'coral_p_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'coral_p_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'geometry_dissolved': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '3857', 'null': 'True', 'blank': 'True'}),
            'geometry_final_area': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lease_blocks': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'mangrove_p': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mangrove_p_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mangrove_p_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': "'255'"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pr_apc_p': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pr_apc_p_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'pr_apc_p_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'pr_ape_p': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pr_ape_p_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'pr_ape_p_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'protarea_p': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'protarea_p_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'protarea_p_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'satisfied': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sharing_groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'scenarios_scenario_related'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.Group']"}),
            'subs_mind': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subs_mind_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'subs_mind_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'subveg_p': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subveg_p_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'subveg_p_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scenarios_scenario_related'", 'to': "orm['auth.User']"}),
            'vi_apc_p': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vi_apc_p_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'vi_apc_p_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'wind_avg': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wind_avg_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'wind_avg_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['scenarios']