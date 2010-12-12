from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.forms import ModelForm
from django import forms
from django.forms.models import ModelChoiceField
from django.contrib.markup.templatetags.markup import textile
from html2text import html2text
from extraformfields import *
from hashlib import md5

class List(models.Model):
	name = models.CharField(max_length=200)
	praefix = models.CharField(max_length=20, verbose_name=_("praefix for subject [...]"))
	footer_text = models.TextField(verbose_name=_("Footer plain text"), blank=True)
	footer_html = models.TextField(verbose_name=_("Footer HTML"), blank=True)
	def __unicode__(self):
		return self.name

class Subscriber(models.Model):
	name = models.CharField(max_length=200,blank=True, verbose_name=_("Name"))
	email = models.EmailField(verbose_name=_("e-Mail Address"))
	subscription = models.ForeignKey(List, default=1, related_name="recipients", verbose_name=_("Subscription"))
	date = models.DateTimeField(auto_now_add=True, editable=False)
	confirmed = models.BooleanField(default=True, editable=True, verbose_name=_("confirmed"))
	token = models.CharField(max_length=12, editable=False)
	def save(self, *args, **kwargs):
		m = md5('%s-%s' % (self.name, self.email))
		self.token = m.hexdigest()[4:16]
		super(Subscriber, self).save(*args, **kwargs) # Call the "real" save() method.
	def __unicode__(self):
		return self.email

class Message(models.Model):
	TEXT_FORMATS = (
		('plain', _('Plain Text')),
		('html', _('HTML')),
		('textile', _('Textile')),
	)
	subject = models.CharField(max_length=200,blank=True, verbose_name=_("Subject"))
	text = models.TextField(verbose_name=_("Text"))
	text_format = models.CharField(max_length=8, choices=TEXT_FORMATS, default="plain", verbose_name=_("Text format"))
	date= models.DateField(auto_now_add=True, editable=False)
	locked = models.BooleanField(default=False, verbose_name=_("locked"))
	@property
	def text_as_html(self):
		if self.text_format == 'plain':
			return u'<pre>%s</pre>' % self.text
		if self.text_format == 'textile':
			return textile(self.text)
		return self.text
	@property
	def text_as_plain(self):
		if self.text_format == 'html':
			return html2text(self.text)
		return self.text
	def __unicode__(self):
		return self.subject

class Attachement(models.Model):
	file = models.FileField(upload_to="attachements", verbose_name=_("File"))
	message = models.ForeignKey(Message, related_name="attachements", verbose_name=_("Message"))
	def __unicode__(self):
		return self.file.name

class Job(models.Model):
	message = models.ForeignKey(Message, verbose_name=_("Message"))
	to = models.ForeignKey(List, verbose_name=_("to List"))
	date = models.DateTimeField(auto_now_add=True, editable=False)
	sender = models.ForeignKey(User, related_name="mailjobs")
	last_delivery = models.DateTimeField(editable=False, blank=True)
	letters_sent = models.IntegerField(default=0, editable=False, blank=True)
	@property
	def active(self):
		return (self.letters.count() > 0)
	def __unicode__(self):
		return u'%s - %s' % (self.to.name, self.message.subject)

class Letter(models.Model):
	job = models.ForeignKey(Job, related_name="letters")
	recipient = models.ForeignKey(Subscriber)
	@property
	def message(self):
		return self.job.message
	def __unicode__(self):
		return u'%s - %s' % (self.recipient.email, self.job.message.subject)


class SubscriberForm(ModelForm):
	class Meta:
		model = Subscriber

class SubscriberFormPublic(ModelForm):
	class Meta:
		model = Subscriber
		fields = ('name', 'email')

class MessageForm(ModelForm):
	class Meta:
		model = Message
		fields = ('subject', 'text', 'text_format')

class JobForm(forms.Form):
	message = FeaturedModelChoiceField(queryset = Message.objects.all(),
		featured_queryset = Message.objects.filter(locked=False),
		label = _('Message'),
	)
	to = ModelChoiceField(queryset = List.objects.all(),
		empty_label = None,
		label = _('To list'),
	)
