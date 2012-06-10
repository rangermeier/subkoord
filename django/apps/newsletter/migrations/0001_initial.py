# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'List'
        db.create_table('newsletter_list', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('praefix', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('footer_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('footer_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('from_address', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('from_bounce_address', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('reply_to_address', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
        ))
        db.send_create_signal('newsletter', ['List'])

        # Adding model 'Subscriber'
        db.create_table('newsletter_subscriber', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('subscription', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='recipients', to=orm['newsletter.List'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=12)),
        ))
        db.send_create_signal('newsletter', ['Subscriber'])

        # Adding model 'Message'
        db.create_table('newsletter_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('text_format', self.gf('django.db.models.fields.CharField')(default='plain', max_length=8)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('locked', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('newsletter', ['Message'])

        # Adding model 'Job'
        db.create_table('newsletter_job', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(related_name='jobs', to=orm['newsletter.Message'])),
            ('to', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['newsletter.List'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mailjobs', to=orm['auth.User'])),
            ('last_delivery', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('letters_sent', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
        ))
        db.send_create_signal('newsletter', ['Job'])

        # Adding model 'Letter'
        db.create_table('newsletter_letter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(related_name='letters', to=orm['newsletter.Job'])),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['newsletter.Subscriber'])),
        ))
        db.send_create_signal('newsletter', ['Letter'])


    def backwards(self, orm):
        # Deleting model 'List'
        db.delete_table('newsletter_list')

        # Deleting model 'Subscriber'
        db.delete_table('newsletter_subscriber')

        # Deleting model 'Message'
        db.delete_table('newsletter_message')

        # Deleting model 'Job'
        db.delete_table('newsletter_job')

        # Deleting model 'Letter'
        db.delete_table('newsletter_letter')


    models = {
        'attachment.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'file': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
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
        'newsletter.job': {
            'Meta': {'object_name': 'Job'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_delivery': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'letters_sent': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'jobs'", 'to': "orm['newsletter.Message']"}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mailjobs'", 'to': "orm['auth.User']"}),
            'to': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['newsletter.List']"})
        },
        'newsletter.letter': {
            'Meta': {'object_name': 'Letter'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'letters'", 'to': "orm['newsletter.Job']"}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['newsletter.Subscriber']"})
        },
        'newsletter.list': {
            'Meta': {'object_name': 'List'},
            'footer_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'footer_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'from_address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'from_bounce_address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'praefix': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'reply_to_address': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'})
        },
        'newsletter.message': {
            'Meta': {'object_name': 'Message'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'text_format': ('django.db.models.fields.CharField', [], {'default': "'plain'", 'max_length': '8'})
        },
        'newsletter.subscriber': {
            'Meta': {'object_name': 'Subscriber'},
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'recipients'", 'to': "orm['newsletter.List']"}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        }
    }

    complete_apps = ['newsletter']