from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext as _
from datetime import date, datetime, timedelta
import vobject
from models import Event, EventForm, EventType, Job, Task, Note, NoteForm
from django.db.models.signals import post_save, post_delete

def clear_cache(sender, **kwargs):
    from django.core.cache import cache
    cache.clear()

post_save.connect(clear_cache)
post_delete.connect(clear_cache)

@login_required
def event_index(request, **kwargs):
    if 'archive' in kwargs.keys():
        event_list = Event.objects.filter(date__lte=datetime.now()).order_by('-date')
    else:
        event_list = Event.objects.filter(date__gte=datetime.now()).order_by('date')
    return render_to_response('event/events.html',
        {'event_list': event_list,
        'archive': 'archive' in kwargs.keys(),
        'date': datetime.today(), },
        context_instance=RequestContext(request),)

@login_required
def event_cal(request, year = False, month = False):
    if not year or not month:
        year = date.today().year
        month = date.today().month
    return render_to_response('event/events_cal.html',
        {'year': int(year),
        'month': int(month),
        'date': datetime.today(), },
        context_instance=RequestContext(request),)

def event_ical(request):
    event_list = Event.objects.filter(date__gte=datetime.now()-timedelta(weeks=4)).order_by('date')
    cal = vobject.iCalendar()
    cal.add('method').value = 'PUBLISH'  # IE/Outlook needs this
    cal.add('x-wr-calname').value = "Subterrarium intern"
    for event in event_list:
        url = settings.SITE_URL + reverse('event', args=[event.id])
        date = event.date - settings.EVENT_TIMEZONE.utcoffset(event.date)
        vevent = cal.add('vevent')
        if event.date.hour == 0 and event.date.minute == 0:
            vevent.add('X-FUNAMBOL-ALLDAY').value = '1'
            vevent.add('dtstart').value = datetime.date(event.date)
            vevent.add('dtend').value = datetime.date(event.date) + timedelta(days=1)
        else:
            vevent.add('dtstart').value = date
            vevent.add('dtend').value = date + timedelta(hours = 2)
        vevent.add('dtstamp').value = datetime.now()
        vevent.add('summary').value = event.title
        vevent.add('url').value = url
        vevent.add('uid').value = "%s-%s" % (event.id, settings.EVENT_REMINDER_FROM)
        vevent.add('description').value = url + "\n" + event.info
    icalstream = cal.serialize()
    response = HttpResponse(icalstream, mimetype='text/calendar; charset=utf-8')
    response['Filename'] = 'subkoordinator.ics'  # IE needs this
    response['Content-Disposition'] = 'attachment; filename=subkoordinator.ics'
    return response

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
def event_delete(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    for job in event.jobs:
        job.delete()
    messages.success(request, _("Event %s deleted" % (event.title)))
    event.delete()
    return HttpResponseRedirect(reverse('event_index'))

@login_required
def event_edit(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event_types = EventType.objects.all()

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, _("Saved changes"))
            return HttpResponseRedirect(reverse('event', args=[event.id]))
    else:
        form = EventForm(instance=event)
    return render_to_response('event/event_edit.html', {
        'form': form,
        'event': event,
        'event_types': event_types,
        },
        context_instance=RequestContext(request),
    )

@login_required
def event_new(request):
    event_types = EventType.objects.all()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            messages.success(request, _("Created new event"))
            return HttpResponseRedirect(reverse('event', args=[event.id]))
    elif 'date' in request.GET:
        form = EventForm(initial={'date': request.GET['date']})
    else:
        form = EventForm()
    return render_to_response('event/event_new.html', {
        'form': form,
        'event_types': event_types,
        },
        context_instance=RequestContext(request),
    )

@login_required
def job_add(request, event_id, task_id):
    event = get_object_or_404(Event, pk=event_id)
    task = get_object_or_404(Task, pk=task_id)
    #job_user = get_object_or_404(User, pk=user_id)

    #if job_user != user:
    #   return HttpResponseNotAllowed('<h1>Must not add other users!</h1>')
    job = Job(event=event, task = task, user = request.user)
    job.save()
    messages.success(request, _("Took job"))
    return HttpResponseRedirect(reverse('event', args=[event.id]))

@login_required
def job_delete(request, event_id, job_id):
    job = get_object_or_404(Job, pk=job_id)

    #if job.user != user:
    #   return HttpResponseNotAllowed('<h1>Must not delete other users\' jobs!</h1>')
    job.delete()
    messages.success(request, _("Deleted job"))
    return HttpResponseRedirect(reverse('event', args=[event_id]))

@login_required
def note_add(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST': # If the form has been submitted...
        form = NoteForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            note = Note(event=event, user=request.user, note = form.cleaned_data['note'])
            note.save()
            messages.success(request, _("Saved note"))
    return HttpResponseRedirect(reverse('event', args=[event.id]))
