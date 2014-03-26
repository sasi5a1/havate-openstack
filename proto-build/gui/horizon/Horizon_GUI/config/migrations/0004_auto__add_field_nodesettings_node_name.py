# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'NodeSettings.node_name'
        db.add_column(u'config_nodesettings', 'node_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'NodeSettings.node_name'
        db.delete_column(u'config_nodesettings', 'node_name')


    models = {
        u'config.nodesettings': {
            'Meta': {'object_name': 'NodeSettings'},
            'aio': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cinder': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'compute': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'network': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'node_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'node_number': ('django.db.models.fields.IntegerField', [], {}),
            'swift': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'config.openstacksettings': {
            'Meta': {'object_name': 'OpenstackSettings'},
            'cluster_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'cluster_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'hostname_prefix_compute_nodes': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'hostname_prefix_swift_nodes': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iscsi_subnet': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'iscsi_vlan': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'kvm_ip_pool': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'kvm_ip_pool_size': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'mac_pool': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'mac_pool_size': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'mgmt_subnet': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'mgmt_vlan': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'os_cluster_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'os_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'private_subnet': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'private_vlan': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'public_provider_subnet': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'public_provider_vlan': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'pxe_subnet': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'pxe_vlan': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'storage_subnet': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'storage_vlan': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'tenants_subnet': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'tenants_vlan': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'ucsm_hostname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        }
    }

    complete_apps = ['config']