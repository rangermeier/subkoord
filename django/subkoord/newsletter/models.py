from django.db import models
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.template import Context, Template
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils.text import get_valid_filename
from django.conf import settings
from django.contrib.contenttypes import generic
from subkoord.attachment.models import Attachment
from html2text import html2text
import random, string
import mimetypes
from datetime import datetime

class List(models.Model):
    name = models.CharField(max_length=200)
    praefix = models.CharField(max_length=20, verbose_name=_("praefix for subject [...]"))
    footer_text = models.TextField(verbose_name=_("Footer plain text"), blank=True)
    footer_html = models.TextField(verbose_name=_("Footer HTML"), blank=True)
    from_address = models.EmailField(verbose_name=_("From e-mail address"))
    from_bounce_address = models.EmailField(verbose_name=_("Technical From e-mail address (used for bounces)"))
    reply_to_address = models.EmailField(verbose_name=_("Reply-to e-mail address"), blank=True)
    def __unicode__(self):
        return self.name

class Subscriber(models.Model):
    """
    >>> list = List(name="Test")
    >>> list.save()
    >>> sub1 = Subscriber(name="Bert", email="bert@foomail.com", subscription=list)
    >>> sub1.save()
    >>> list.recipients.all()
    [<Subscriber: bert@foomail.com>]
    >>> sub2 = Subscriber(name="Sue", email="sue@foomail.com", subscription=list)
    >>> sub2.save()
    >>> list.recipients.all()
    [<Subscriber: bert@foomail.com>, <Subscriber: sue@foomail.com>]
    """
    name = models.CharField(max_length=200,blank=True, verbose_name=_("Name"), help_text=_("(optional)"))
    email = models.EmailField(verbose_name=_("e-Mail Address"))
    subscription = models.ForeignKey(List, default=1, related_name="recipients", verbose_name=_("Subscription"))
    date = models.DateTimeField(auto_now_add=True, editable=False)
    confirmed = models.BooleanField(default=True, editable=True, verbose_name=_("confirmed"))
    token = models.CharField(max_length=12, editable=False)
    def save(self, *args, **kwargs):
        alnum = string.letters + string.digits
        self.token = ''.join(random.choice(alnum) for i in range(Subscriber._meta.get_field("token").max_length))
        super(Subscriber, self).save(*args, **kwargs) # Call the "real" save() method.
    def __unicode__(self):
        return self.email

class Message(models.Model):
    subject = models.CharField(max_length=200,blank=True, verbose_name=_("Subject"))
    text = models.TextField(verbose_name=_("Text"))
    date= models.DateField(auto_now_add=True, editable=False)
    locked = models.BooleanField(default=False, verbose_name=_("locked"))
    attachments = generic.GenericRelation(Attachment)
    @property
    def active_jobs(self):
        try:
            self._active_jobs
        except AttributeError:
            self._active_jobs = [job for job in self.jobs.all()
                if job.active]
        return self._active_jobs
    @property
    def finished_jobs(self):
        try:
            self._finished_jobs
        except AttributeError:
            self._finished_jobs = [job for job in self.jobs.all()
                if not job.active]
        return self._finished_jobs
    @property
    def in_delivery(self):
        for job in self.jobs.all():
            if job.active:
                return True
        return False
    @property
    def text_as_plain(self):
        return html2text(self.text)
    def __unicode__(self):
        return self.subject



class Job(models.Model):
    """
    >>> message = Message(subject="Concert!", text="Hi, it's gonna be great")
    >>> message.save()
    >>> list = List(name="Test")
    >>> list.save()
    >>> sub1 = Subscriber(name="Bert", email="bert@foomail.com", subscription=list)
    >>> sub1.save()
    >>> sub2 = Subscriber(name="Sue", email="sue@foomail.com", subscription=list)
    >>> sub2.save()
    >>> hugo = User(username="hugo")
    >>> hugo.save()
    >>> job = Job(message=message, to=list, sender=hugo)
    >>> job.save()
    >>> job.letters_total
    2
    >>> job.active
    True
    """
    message = models.ForeignKey(Message, related_name="jobs", verbose_name=_("Message"))
    to = models.ForeignKey(List, verbose_name=_("to List"))
    date = models.DateTimeField(auto_now_add=True, editable=False)
    sender = models.ForeignKey(User, related_name="mailjobs")
    last_delivery = models.DateTimeField(editable=False, null=True)
    letters_sent = models.IntegerField(default=0, editable=False, blank=True)
    @property
    def letters_total(self):
        try:
            self._letters_total
        except AttributeError:
            self._letters_total = self.letters.count() + self.letters_sent
        return self._letters_total
    @property
    def percent_sent(self):
        if self.letters_total == 0 or not self.active:
            return 100
        try:
            self._percent_sent
        except AttributeError:
            self._percent_sent = int((float(self.letters_sent)/self.letters_total)*100)
        return self._percent_sent
    @property
    def active(self):
        try:
            self._active
        except AttributeError:
            self._active = (self.letters.count() > 0)
        return self._active
    def save(self, *args, **kwargs):
        create_letters = not bool(self.__getattribute__('id'))
        super(Job, self).save(*args, **kwargs) # Call the "real" save() method.
        if create_letters:
            letters = []
            for recipient in self.to.recipients.filter(confirmed=True):
                letters.append(Letter(job=self, recipient=recipient))
            Letter.objects.bulk_create(letters)
            self.message.locked = True
            self.message.save()
    def __unicode__(self):
        return u'%s - %s' % (self.to.name, self.message.subject)

class Letter(models.Model):
    job = models.ForeignKey(Job, related_name="letters")
    recipient = models.ForeignKey(Subscriber)
    @property
    def message(self):
        return self.job.message
    def send(self):
        footer_text = Template(self.job.to.footer_text)
        footer_html = Template(self.job.to.footer_html)
        c = Context({
            'unsubscribe_url': settings.SITE_URL+reverse('subscriber_public_delete', args=[self.recipient.id, self.recipient.token]),
        })
        text_plain = "\n".join([self.message.text_as_plain, footer_text.render(c)])
        text_html = "\n<br>\n".join([self.message.text, footer_html.render(c)])
        mail = EmailMultiAlternatives(
            subject = u'%s %s' % (self.job.to.praefix, self.message.subject),
            body = text_plain,
            from_email = u'sid_%s_%s' % (self.recipient.id, self.job.to.from_bounce_address),
            to = [self.recipient.email],
            headers = {'Reply-To': self.job.to.reply_to_address,
                'From': self.job.to.from_address},
        )
        for attachment in self.message.attachments.all():
            mail.attach_file(attachment.file.path)
        mail.attach_alternative(text_html, "text/html")
        mail.send()
        self.job.letters_sent += 1
        self.job.last_delivery = datetime.now()
        self.job.save()
    def __unicode__(self):
        return u'%s - %s' % (self.recipient.email, self.job.message.subject)
