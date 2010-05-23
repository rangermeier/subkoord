from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
#from django.contrib import messages # Django 1.2
from datetime import date, datetime
from models import Event, EventForm, Job, Task, Note, NoteForm

@login_required
def event_index(request, **kwargs):
	if 'archive' in kwargs.keys():
		event_list = Event.objects.filter(date__lte=datetime.now())
	else:
		event_list = Event.objects.filter(date__gte=datetime.now())
	return render_to_response('event/events.html',
		{'event_list': event_list,
		'archive': 'archive' in kwargs.keys(), },
		context_instance=RequestContext(request),)

@login_required
def event_cal(request, year = False, month = False):
	if not year or not month:
		year = date.today().year
		month = date.today().month
	return render_to_response('event/events_cal.html',
		{'year': int(year),
		'month': int(month) },
		context_instance=RequestContext(request),)

@login_required
def event(request, event_id):
	event = get_object_or_404(Event, pk=event_id)
	user_tasks = []
	for job in event.job_set.filter(user=request.user.id).values('task'):
		user_tasks.append(job['task'])
	return render_to_response('event/event.html',
		{'event': event,
		'user_tasks': user_tasks, },
		context_instance=RequestContext(request), )

@login_required
def event_edit(request, event_id):
	event = get_object_or_404(Event, pk=event_id)

	if request.method == 'POST':
		form = EventForm(request.POST, instance=event)
		if form.is_valid():
			form.save()
			request.user.message_set.create(message="Saved changes") # Django 1.1
			return HttpResponseRedirect(reverse('event', args=[event.id]))
	else:
		form = EventForm(instance=event)
	return render_to_response('event/event_edit.html', {
		'form': form,
		'event': event,
		},
		context_instance=RequestContext(request),
	)

@login_required
def event_new(request):
	if request.method == 'POST':
		form = EventForm(request.POST)
		if form.is_valid():
			form.save()
			request.user.message_set.create(message="Created new event") # Django 1.1
			return HttpResponseRedirect(reverse('event_index'))
	else:
		form = EventForm()
	return render_to_response('event/event_new.html', {
		'form': form,
		},
		context_instance=RequestContext(request),
	)

@login_required
def job_add(request, event_id, task_id):
	event = get_object_or_404(Event, pk=event_id)
	task = get_object_or_404(Task, pk=task_id)
	#job_user = get_object_or_404(User, pk=user_id)

	#if job_user != user:
	#	return HttpResponseNotAllowed('<h1>Must not add other users!</h1>')
	job = Job(event=event, task = task, user = request.user)
	job.save()
	# Django 1.1 messages.add_message(request, messages.INFO, 'Added user')
	request.user.message_set.create(message="Took job") # Django 1.1
	return HttpResponseRedirect(reverse('event', args=[event.id]))

@login_required
def job_delete(request, event_id, job_id):
	job = get_object_or_404(Job, pk=job_id)

	#if job.user != user:
	#	return HttpResponseNotAllowed('<h1>Must not delete other users\' jobs!</h1>')
	job.delete()
	# Django 1.2: messages.add_message(request, messages.INFO, 'Deleted job')
	request.user.message_set.create(message="Deleted job") # Django 1.1
	return HttpResponseRedirect(reverse('event', args=[event_id]))

@login_required
def note_add(request, event_id):
	event = get_object_or_404(Event, pk=event_id)
	if request.method == 'POST': # If the form has been submitted...
		form = NoteForm(request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			note = Note(event=event, user=request.user, note = form.cleaned_data['note'])
			note.save()
			request.user.message_set.create(message="Saved note") # Django 1.1
	return HttpResponseRedirect(reverse('event', args=[event.id]))
