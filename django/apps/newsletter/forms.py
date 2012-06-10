from django import forms
from django.forms import ModelForm
from django.forms.models import ModelChoiceField
from django.forms.fields import IntegerField, FileField
from django.db.models import Count
from django.conf import settings
from django.utils.translation import ugettext as _
from extraformfields import *
from models import Subscriber, Message, List
from bootstrap.forms import BootstrapMixin, BootstrapForm
from tinymce.widgets import TinyMCE

class SubscriberForm(BootstrapMixin, ModelForm):
    class Meta:
        model = Subscriber

class SubscriberFormPublic(BootstrapMixin, ModelForm):
    class Meta:
        model = Subscriber
        fields = ('name', 'email')

class MessageForm(BootstrapMixin, ModelForm):
    class Meta:
        model = Message
        fields = ('subject', 'text')
        widgets = {
            'text': TinyMCE(mce_attrs={
                    'plugins': "paste",
                    'theme_advanced_buttons1' : "cut,copy,paste,pastetext,pasteword,|,undo,redo,|,link,unlink|,code,cleanup,removeformat",
                    'theme_advanced_buttons2' : "bold,italic,underline,strikethrough,|,bullist,numlist,|,outdent,indent,blockquote,|,hr",
                    'theme_advanced_buttons3' : None,
            }),
        }

class JobForm(BootstrapMixin, forms.Form):
    message = FeaturedModelChoiceField(queryset = Message.objects.all(),
        featured_queryset = Message.objects.filter(locked=False),
        label = _('Message'),
    )
    to = ModelChoiceField(queryset = List.objects.all(),
        label = _('To list'),
    )

class JobMessageForm(BootstrapForm):
    message = IntegerField(widget = forms.HiddenInput,)
    to = ModelChoiceField(queryset = List.objects.all(),
        label = _('To list'),
    )

class PreviewMessageForm(BootstrapForm):
    message = IntegerField(widget = forms.HiddenInput,)
    to = ModelChoiceField(queryset =
        List.objects.annotate(recipients_count=Count('recipients')).filter(recipients_count__lt=settings.NEWSLETTER_PREVIEW_LIST),
        label = _('To list'),
    )
