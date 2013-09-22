# coding=utf-8
import os
from django import forms
from django.forms import ModelForm
from django.forms.models import modelformset_factory
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _
from django.conf import settings
from models import Attachment


class AttachmentForm(ModelForm):
    def clean_file(self):
        file = self.cleaned_data['file']
        if len(file) == 0:
            return file
        try:
            f = open(os.path.join(settings.MEDIA_ROOT, file))
            return file
        except IOError:
            raise forms.ValidationError(_(u'%s does not exist. Please choose another file or delete attachment.' % file))
    class Meta:
        model = Attachment
        fields = ('file', )


AttachmentFormSet = modelformset_factory(Attachment,
    form = AttachmentForm,
    can_delete=True)

"""
ertellt Formular für Anhänge und speichert dieses
Parameter: ein RequestObject und das Objekt zu dem die Attachments gehören
Rückgabe: ein Formset
"""
def attachment_formset_handler(request, object):
    if request.method == "POST" and request.POST.has_key("attachments-TOTAL_FORMS"):
        attachment_formset = AttachmentFormSet(request.POST, prefix = "attachments" )
        if attachment_formset.is_valid():
            for form in attachment_formset:
                if form.cleaned_data.has_key("id") and form.cleaned_data["id"]:
                    if not form.cleaned_data["file"] or form.cleaned_data["DELETE"] == True:
                        form.cleaned_data["id"].delete()
                    else:
                        form.save()
                elif form.cleaned_data.has_key("file") and form.cleaned_data["file"]:
                    if not object.id:
                        object.save()
                    attachment = Attachment(file = form.cleaned_data["file"],
                        content_type = ContentType.objects.get_for_model(object),
                        object_id = object.id, )
                    attachment.save()
    else:
        attachment_formset = AttachmentFormSet(queryset = object.attachments.all(),
            prefix = "attachments" )
    return attachment_formset
