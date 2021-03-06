# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Eenheid', fields ['naam']
        db.create_unique(u'producten_eenheid', ['naam'])

        # Adding unique constraint on 'Eenheid', fields ['afkorting']
        db.create_unique(u'producten_eenheid', ['afkorting'])


    def backwards(self, orm):
        # Removing unique constraint on 'Eenheid', fields ['afkorting']
        db.delete_unique(u'producten_eenheid', ['afkorting'])

        # Removing unique constraint on 'Eenheid', fields ['naam']
        db.delete_unique(u'producten_eenheid', ['naam'])


    models = {
        u'producten.eenheid': {
            'Meta': {'object_name': 'Eenheid'},
            'afkorting': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'naam': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'producten.leverancier': {
            'Meta': {'object_name': 'Leverancier'},
            'adres': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'contactpersoon': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'unique': 'True', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'naam': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'telefoon': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        u'producten.samengesteldproduct': {
            'Meta': {'ordering': "['naam']", 'object_name': 'SamengesteldProduct'},
            'beschrijving': ('django.db.models.fields.CharField', [], {'max_length': '4000', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['producten.SimpelProduct']", 'through': u"orm['producten.SamengesteldProductLijn']", 'symmetrical': 'False'}),
            'naam': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'producten.samengesteldproductlijn': {
            'Meta': {'object_name': 'SamengesteldProductLijn'},
            'aantal': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'samengesteldProduct': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['producten.SamengesteldProduct']"}),
            'simpelProduct': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['producten.SimpelProduct']"})
        },
        u'producten.simpelproduct': {
            'Meta': {'unique_together': "(['naam', 'leverancier'],)", 'object_name': 'SimpelProduct'},
            'beschrijving': ('django.db.models.fields.CharField', [], {'max_length': '4000', 'null': 'True'}),
            'eenheid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['producten.Eenheid']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'laatste_aanpassing': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'leverancier': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['producten.Leverancier']"}),
            'naam': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'prijs': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'})
        }
    }

    complete_apps = ['producten']