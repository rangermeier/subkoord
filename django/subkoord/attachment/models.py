from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _
from filebrowser.fields import FileBrowseField

class Attachment(models.Model):
	file = FileBrowseField(_("File"), max_length=200, blank=True)
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = generic.GenericForeignKey('content_type', 'object_id')
	@property
	def mimetype(self):
		return self.file.mimetype
	@property
	def is_image(self):
		return self.file.filetype == 'Image'
	def __unicode__(self):
		return self.file.filename
