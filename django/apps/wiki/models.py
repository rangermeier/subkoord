# http://news.e-scribe.com/210

from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import ugettext as _
from django.contrib.contenttypes import generic
from attachment.models import Attachment
from tinymce.widgets import TinyMCE

class Wikicategory(models.Model):
    """Category for pages"""
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class Wikipage(models.Model):
    """Wiki page storage"""
    title = models.SlugField(max_length=50, unique = True, verbose_name=_("Page Title"),
        help_text=_("Only letters, numbers, underscores and hyphens."))
    content_html = models.TextField(verbose_name=_("Content"))
    last_changed = models.DateTimeField(auto_now=True, editable=False)
    author = models.ForeignKey(User, editable=False)
    category = models.ForeignKey(Wikicategory, null=True, verbose_name=_("Category"))
    attachments = generic.GenericRelation(Attachment)

    def __unicode__(self):
        return self.title

class WikipageForm(ModelForm):
    class Meta:
        model = Wikipage
        widgets = {
            'content_html': TinyMCE(attrs={"rows": 20, "cols": "80"}),
        }
