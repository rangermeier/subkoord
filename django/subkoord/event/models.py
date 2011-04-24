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
	def maxed_out(self, event):
		try:
			self._maxed_out[event.id]
		except AttributeError:
			self._maxed_out = {}
			return self.maxed_out(event)
		except KeyError:
			if type(self.max_persons) != type(1L):
				self._maxed_out[event.id] = False
			else:
				self._maxed_out[event.id] = self.job_set.filter(event=event.id).count() >= self.max_persons
		return self._maxed_out[event.id]
	def satisfied(self, event):
		try:
			self._satisfied[event.id]
		except AttributeError:
			self._satisfied = {}
			return self.satisfied(event)
		except KeyError:
			if type(self.min_persons) != type(1L):
				self._satisfied[event.id] = True
			else:
				self._satisfied[event.id] = self.job_set.filter(event=event.id).count() >= self.min_persons
		return self._satisfied[event.id]
	def clear_buffer(self):
		try:
			self.__delattr__("_maxed_out")
			self.__delattr__("_satisfied")
		except AttributeError:
			pass
	def __unicode__(self):
		return self.name


class EventType(models.Model):
	name = models.CharField(max_length=200)
	info = models.TextField(blank=True)
	tasks = models.ManyToManyField(Task, blank=True, related_name='types')
	def __unicode__(self):
		return self.name

class Event(models.Model):
	title = models.CharField(verbose_name=_("Title"), max_length=200)
	date = models.DateTimeField(verbose_name=_("Date and Time"))
	type = models.ForeignKey(EventType, verbose_name=_("Type"),
		help_text=_("Depending on the type of the event different tasks will be available."))
	info = models.TextField(verbose_name=_("Information"), blank=True,
		help_text=_("You can use Textile to format your text."))
	cron = models.DateTimeField(blank=True, null=True, editable=False)
	@property
	def tasks(self):
		try:
			self._tasks
		except AttributeError:
			self._tasks = self.type.tasks.select_related().all()
		return self._tasks
	@property
	def open_tasks(self):
		try:
			self._open_tasks
		except AttributeError:
			self._open_tasks = []
			for task in self.tasks:
				if not task.satisfied(self):
					self._open_tasks.append(task)
		return self._open_tasks
	def clear_buffer(self):
		try:
			self.__delattr__("_tasks")
			self.__delattr__("_open_tasks")
		except AttributeError:
			pass
	@property
	def all_tasks_satisfied(self):
		return (len(self.open_tasks) == 0)
	@property
	def jobs(self):
		return self.job_set.all()
	def __unicode__(self):
		return self.title

class Job(models.Model):
	event = models.ForeignKey(Event)
	task = models.ForeignKey(Task)
	user = models.ForeignKey(User, related_name="jobs")
	def delete(self, *args, **kwargs):
		self.task.clear_buffer()
		self.event.clear_buffer()
		super(Job, self).delete(*args, **kwargs) # Call the "real" delete() method
	def save(self, *args, **kwargs):
		self.task.clear_buffer()
		self.event.clear_buffer()
		super(Job, self).save(*args, **kwargs) # Call the "real" save() method.
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
