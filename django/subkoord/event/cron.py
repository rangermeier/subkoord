from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.utils.translation import ugettext as _
from models import Event

def render_to_email(view,subject,to_emails,from_email,*args,**kwargs):
	"""
	Renders a view to an email
	Example:
	render_to_email("myview.html","the subject",("to_example@example.com",),"from@example.com",{},context=RequestContext(request))
	"""
	body=loader.render_to_string(view,*args,**kwargs)
	send_mail(subject,body,from_email,to_emails)

def cron(request):
	remind_window = timedelta(days=2) # when to start bragging
	remind_pause = timedelta(days=1) # how often cron should run at max
	subject = _("Open Tasks")
	events = Event.objects.select_related(
		).filter(
			date__gte = datetime.now()
		).filter(
			date__lte = datetime.now() + remind_window
		).exclude(
			cron__gte = datetime.now() - remind_pause
		)
	for event in events:
		if event.all_tasks_satisfied:
			events = events.exclude(id=event.id)
	if events.count() > 0:
		#adressbook = []
		#users = User.objects.all()
		#for user in users:
		#	adressbook.append(user.email)
		adressbook = ["subterrarium@googlegroups.com"]
		render_to_email("email/open_tasks.html",
			subject,
			adressbook,
			"subkoord@powidl.org",
			{'events': events, 'site_url': 'http://subkoord.powidl.org',},
		)
		for event in events:
		  event.cron = datetime.now()
		  event.save()
		return render_to_response('email/open_tasks.html', {
			'events': events,
			'site_url': 'http://subkoord.powidl.org',
			},
			context_instance=RequestContext(request),
		)
	else:
		return HttpResponse("no open tasks")
