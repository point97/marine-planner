# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'KMLCache'
        db.create_table('scenarios_kmlcache', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('val', self.gf('picklefield.fields.PickledObjectField')()),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('scenarios', ['KMLCache'])

        # Adding model 'Scenario'
        db.create_table('scenarios_scenario', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='scenarios_scenario_related', to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length='255')),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='scenarios_scenario_related', null=True, to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('input_parameter_depth', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('input_min_depth', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('input_max_depth', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('input_parameter_distance_to_shore', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('input_min_distance_to_shore', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('input_max_distance_to_shore', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('input_parameter_wind_speed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('input_avg_wind_speed', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('input_filter_uxo', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('satisfied', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('lease_blocks', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('geometry_final_area', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('geometry_dissolved', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(srid=3857, null=True, blank=True)),
        ))
        db.send_create_signal('scenarios', ['Scenario'])

        # Adding M2M table for field sharing_groups on 'Scenario'
        m2m_table_name = db.shorten_name('scenarios_scenario_sharing_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('scenario', models.ForeignKey(orm['scenarios.scenario'], null=False)),
            ('group', models.ForeignKey(orm['auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['scenario_id', 'group_id'])

        # Adding model 'Objective'
        db.create_table('scenarios_objective', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('color', self.gf('django.db.models.fields.CharField')(default='778B1A55', max_length=8)),
        ))
        db.send_create_signal('scenarios', ['Objective'])

        # Adding model 'Parameter'
        db.create_table('scenarios_parameter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ordering_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=35, null=True, blank=True)),
            ('shortname', self.gf('django.db.models.fields.CharField')(max_length=35, null=True, blank=True)),
        ))
        db.send_create_signal('scenarios', ['Parameter'])

        # Adding M2M table for field objectives on 'Parameter'
        m2m_table_name = db.shorten_name('scenarios_parameter_objectives')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('parameter', models.ForeignKey(orm['scenarios.parameter'], null=False)),
            ('objective', models.ForeignKey(orm['scenarios.objective'], null=False))
        ))
        db.create_unique(m2m_table_name, ['parameter_id', 'objective_id'])

        # Adding model 'LeaseBlock'
        db.create_table('scenarios_leaseblock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('wind_min', self.gf('django.db.models.fields.FloatField')()),
            ('wind_max', self.gf('django.db.models.fields.FloatField')()),
            ('wind_avg', self.gf('django.db.models.fields.FloatField')()),
            ('bathy_min', self.gf('django.db.models.fields.IntegerField')()),
            ('bathy_max', self.gf('django.db.models.fields.IntegerField')()),
            ('bathy_avg', self.gf('django.db.models.fields.FloatField')()),
            ('mangrove_p', self.gf('django.db.models.fields.FloatField')()),
            ('coral_p', self.gf('django.db.models.fields.FloatField')()),
            ('subveg_p', self.gf('django.db.models.fields.FloatField')()),
            ('protarea_p', self.gf('django.db.models.fields.FloatField')()),
            ('subs_minid', self.gf('django.db.models.fields.IntegerField')()),
            ('subs_mind', self.gf('django.db.models.fields.FloatField')()),
            ('subs_avgid', self.gf('django.db.models.fields.IntegerField')()),
            ('subs_avgd', self.gf('django.db.models.fields.FloatField')()),
            ('coast_min', self.gf('django.db.models.fields.FloatField')()),
            ('coast_avg', self.gf('django.db.models.fields.FloatField')()),
            ('pr_apc_p', self.gf('django.db.models.fields.FloatField')()),
            ('pr_ape_p', self.gf('django.db.models.fields.FloatField')()),
            ('vi_apc_p', self.gf('django.db.models.fields.FloatField')()),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(srid=3857, null=True, blank=True)),
        ))
        db.send_create_signal('scenarios', ['LeaseBlock'])


    def backwards(self, orm):
        # Deleting model 'KMLCache'
        db.delete_table('scenarios_kmlcache')

        # Deleting model 'Scenario'
        db.delete_table('scenarios_scenario')

        # Removing M2M table for field sharing_groups on 'Scenario'
        db.delete_table(db.shorten_name('scenarios_scenario_sharing_groups'))

        # Deleting model 'Objective'
        db.delete_table('scenarios_objective')

        # Deleting model 'Parameter'
        db.delete_table('scenarios_parameter')

        # Removing M2M table for field objectives on 'Parameter'
        db.delete_table(db.shorten_name('scenarios_parameter_objectives'))

        # Deleting model 'LeaseBlock'
        db.delete_table('scenarios_leaseblock')


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
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'scenarios_scenario_related'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'geometry_dissolved': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '3857', 'null': 'True', 'blank': 'True'}),
            'geometry_final_area': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input_avg_wind_speed': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'input_filter_uxo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'input_max_depth': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'input_max_distance_to_shore': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'input_min_depth': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'input_min_distance_to_shore': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'input_parameter_depth': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'input_parameter_distance_to_shore': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'input_parameter_wind_speed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lease_blocks': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': "'255'"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'satisfied': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sharing_groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'scenarios_scenario_related'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.Group']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scenarios_scenario_related'", 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['scenarios']