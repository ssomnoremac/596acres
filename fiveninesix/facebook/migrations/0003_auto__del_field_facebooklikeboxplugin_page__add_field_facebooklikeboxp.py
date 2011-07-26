# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'FacebookLikeboxPlugin.page'
        db.delete_column('cmsplugin_facebooklikeboxplugin', 'page')

        # Adding field 'FacebookLikeboxPlugin.url'
        db.add_column('cmsplugin_facebooklikeboxplugin', 'url', self.gf('django.db.models.fields.URLField')(default='', max_length=200), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'FacebookLikeboxPlugin.page'
        db.add_column('cmsplugin_facebooklikeboxplugin', 'page', self.gf('django.db.models.fields.CharField')(default='', max_length=256), keep_default=False)

        # Deleting field 'FacebookLikeboxPlugin.url'
        db.delete_column('cmsplugin_facebooklikeboxplugin', 'url')


    models = {
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'facebook.facebookaccount': {
            'Meta': {'object_name': 'FacebookAccount'},
            'facebookId': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'facebook.facebooklikeboxplugin': {
            'Meta': {'object_name': 'FacebookLikeboxPlugin', 'db_table': "'cmsplugin_facebooklikeboxplugin'", '_ormbases': ['cms.CMSPlugin']},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'facebook.facebookphotoplugin': {
            'Meta': {'object_name': 'FacebookPhotoPlugin', 'db_table': "'cmsplugin_facebookphotoplugin'", '_ormbases': ['cms.CMSPlugin']},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['facebook.FacebookAccount']"}),
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['facebook']