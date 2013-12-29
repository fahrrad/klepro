# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'SimpelProduct.laatste_aanpassing'
        db.add_column(u'producten_simpelproduct', 'laatste_aanpassing',
                      self.gf('django.db.models.fields.DateField')(auto_now=True, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'SimpelProduct.laatste_aanpassing'
        db.delete_column(u'producten_simpelproduct', 'laatste_aanpassing')


    models = {
        u'producten.eenheid': {
            'Meta': {'object_name': 'Eenheid'},
            'afkorting': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'naam': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'producten.leverancier': {
            'Meta': {'object_name': 'Leverancier'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'naam': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'producten.samengesteldproduct': {
            'Meta': {'ordering': "['naam']", 'object_name': 'SamengesteldProduct'},
            'beschrijving': ('django.db.models.fields.CharField', [], {'max_length': '4000', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['producten.SimpelProduct']", 'through': u"orm['producten.SamengesteldProductLijn']", 'symmetrical': 'False'}),
            'naam': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'producten.samengesteldproductlijn': {
            'Meta': {'object_name': 'SamengesteldProductLijn'},
            'aantal': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'samengesteldProduct': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['producten.SamengesteldProduct']"}),
            'simpelProduct': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['producten.SimpelProduct']"})
        },
        u'producten.simpelproduct': {
            'Meta': {'ordering': "['naam']", 'object_name': 'SimpelProduct'},
            'beschrijving': ('django.db.models.fields.CharField', [], {'max_length': '4000', 'null': 'True'}),
            'eenheid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['producten.Eenheid']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'laatste_aanpassing': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'leverancier': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['producten.Leverancier']"}),
            'naam': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'prijs': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'})
        }
    }

    complete_apps = ['producten']