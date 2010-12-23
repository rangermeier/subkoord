from django import forms
from django.forms import ModelForm
from django.forms.models import ModelChoiceField
from django.forms.fields import IntegerField
from django.db.models import Count
from django.conf import settings
from django.utils.translation import ugettext as _
from extraformfields import *
from models import Subscriber, Message, List

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

class JobMessageForm(forms.Form):
	message = IntegerField(widget = forms.HiddenInput,)
	to = ModelChoiceField(queryset = List.objects.all(),
		empty_label = None,
		label = _('To list'),
	)

class PreviewMessageForm(forms.Form):
	message = IntegerField(widget = forms.HiddenInput,)
	to = ModelChoiceField(queryset =
		List.objects.annotate(recipients_count=Count('recipients')).filter(recipients_count__lt=settings.NEWSLETTER_PREVIEW_LIST),
		empty_label = None,
		label = _('To list'),
	)
