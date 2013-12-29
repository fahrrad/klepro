# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Eenheid'
        db.create_table(u'producten_eenheid', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('naam', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('afkorting', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal(u'producten', ['Eenheid'])

        # Adding model 'Leverancier'
        db.create_table(u'producten_leverancier', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('naam', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'producten', ['Leverancier'])

        # Adding model 'SimpelProduct'
        db.create_table(u'producten_simpelproduct', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('naam', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('beschrijving', self.gf('django.db.models.fields.CharField')(max_length=4000, null=True)),
            ('leverancier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['producten.Leverancier'])),
            ('prijs', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('eenheid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['producten.Eenheid'])),
        ))
        db.send_create_signal(u'producten', ['SimpelProduct'])

        # Adding model 'SamengesteldProductLijn'
        db.create_table(u'producten_samengesteldproductlijn', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('simpelProduct', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['producten.SimpelProduct'])),
            ('samengesteldProduct', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['producten.SamengesteldProduct'])),
            ('aantal', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'producten', ['SamengesteldProductLijn'])

        # Adding model 'SamengesteldProduct'
        db.create_table(u'producten_samengesteldproduct', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('naam', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('beschrijving', self.gf('django.db.models.fields.CharField')(max_length=4000, null=True)),
        ))
        db.send_create_signal(u'producten', ['SamengesteldProduct'])


    def backwards(self, orm):
        # Deleting model 'Eenheid'
        db.delete_table(u'producten_eenheid')

        # Deleting model 'Leverancier'
        db.delete_table(u'producten_leverancier')

        # Deleting model 'SimpelProduct'
        db.delete_table(u'producten_simpelproduct')

        # Deleting model 'SamengesteldProductLijn'
        db.delete_table(u'producten_samengesteldproductlijn')

        # Deleting model 'SamengesteldProduct'
        db.delete_table(u'producten_samengesteldproduct')


    models = {
        u'producten.eenheid': {
            'Meta': {'object_name': 'Eenheid'},
            'afkorting': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'naam': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'producten.leverancier': {
            'Meta': {'object_name': 'Leverancier'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'naam': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'producten.samengesteldproduct': {
            'Meta': {'object_name': 'SamengesteldProduct'},
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
            'Meta': {'object_name': 'SimpelProduct'},
            'beschrijving': ('django.db.models.fields.CharField', [], {'max_length': '4000', 'null': 'True'}),
            'eenheid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['producten.Eenheid']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leverancier': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['producten.Leverancier']"}),
            'naam': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'prijs': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'})
        }
    }

    complete_apps = ['producten']