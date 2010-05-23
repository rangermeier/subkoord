from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext as _
from django.forms import ModelForm

class Task(models.Model):
	name = models.CharField(max_length=200)
	info = models.TextField(blank=True)
	min_persons = models.IntegerField(blank=True, null=True)
	max_persons = models.IntegerField(blank=True, null=True)
	@property
	def maxed_out(self):
		return len(self.job_set.all()) >= int(self.max_persons)
	@property
	def satisfied(self):
		return len(self.job_set.all()) >= int(self.min_persons)
	def __unicode__(self):
		return self.name


class EventType(models.Model):
	name = models.CharField(max_length=200)
	info = models.TextField(blank=True)
	tasks = models.ManyToManyField(Task, related_name='types')
	def __unicode__(self):
		return self.name

class Event(models.Model):
	title = models.CharField(max_length=200)
	date = models.DateTimeField()
	info = models.TextField(blank=True)
	type = models.ForeignKey(EventType)
	cron = models.DateTimeField(blank=True, null=True, editable=False)
	@property
	def tasks(self):
		return self.type.tasks.select_related().all()
	@property
	def opentasks(self):
		opentasks = []
		for task in self.tasks:
			if not task.satisfied:
				opentasks.append(task)
		return opentasks
	@property
	def all_tasks_satisfied(self):
		return (len(self.opentasks) == 0)
	@property
	def jobs(self):
		return self.job_set.all()
	def __unicode__(self):
		return self.title

class Job(models.Model):
	event = models.ForeignKey(Event)
	task = models.ForeignKey(Task)
	user = models.ForeignKey(User)
	def __unicode__(self):
		return u'%s - %s: %s' % (self.event.title, self.task.name, self.user.username)

class Note(models.Model):
	event = models.ForeignKey(Event, related_name="notes")
	user = models.ForeignKey(User)
	note = models.TextField()
	date = models.DateTimeField(auto_now_add=True, editable=False)
	def __unicode__(self):
		return self.note[:25] + "..."

class EventForm(ModelForm):
	class Meta:
		model = Event

class NoteForm(forms.Form):
    note = forms.CharField()

