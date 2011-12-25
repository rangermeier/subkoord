# http://news.e-scribe.com/210

from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import ugettext as _
from django.contrib.contenttypes import generic
from attachment.models import Attachment

class Wikicategory(models.Model):
    """Category for pages"""
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class Wikipage(models.Model):
    """Wiki page storage"""
    title = models.SlugField(max_length=50, unique = True, name=_("Title"), verbose_name=_("Page Title"),
        help_text=_("Only letters, numbers, underscores and hyphens."))
    content = models.TextField(name=_("Content"), verbose_name=_("Content"),
        help_text=_("You can use Textile to format your text.")+"<br />"+_("Wiki-Link: <code>[[link_title]]</code>"))
    content_html = models.TextField(name=_("Content"), editable=False)
    last_changed = models.DateTimeField(auto_now=True, editable=False)
    author = models.ForeignKey(User, editable=False)
    category = models.ForeignKey(Wikicategory, null=True, name=_("Category"), verbose_name=_("Category"))
    attachments = generic.GenericRelation(Attachment)

    def __unicode__(self):
        return self.title

class WikipageForm(ModelForm):
    class Meta:
        model = Wikipage
