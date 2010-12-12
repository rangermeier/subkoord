from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.utils.translation import ugettext as _
from datetime import date, datetime
from models import *


@permission_required('newsletter.add_subscriber')
def index(request):
	job_list = Job.objects.all().order_by('-date')[:3]
	unsent_messages = Message.objects.filter(locked=False)
	subscribers = Subscriber.objects.all().order_by('-date')[:10]
	lists = List.objects.all()
	return render_to_response('newsletter/index.html',
		{'job_list': job_list,
		'unsent_messages': unsent_messages,
		'lists': lists,
		'subscribers': subscribers,},
		context_instance=RequestContext(request),)

@permission_required('newsletter.add_message')
def message_new(request):
	if request.method == "POST":
		message_form = MessageForm(request.POST)
		if message_form.is_valid():
			message = message_form.save()
			return HttpResponseRedirect(reverse('message', args=[message.id]))
	else:
		message_form = MessageForm()
	return render_to_response('newsletter/message.html',
		{'message_form': message_form, },
		context_instance=RequestContext(request),)

@permission_required('newsletter.add_message')
def message(request, message_id):
	MessageFormSet = inlineformset_factory(Message, Attachement, extra=1)
	message = get_object_or_404(Message, pk=message_id)
	if not message.locked and request.method == "POST":
		message_form = MessageForm(request.POST, instance=message)
		message_formset = MessageFormSet(request.POST, request.FILES, instance=message)
		if message_form.is_valid() and message_formset.is_valid():
			message_form.save()
			message_formset.save()
			return HttpResponseRedirect(reverse('message', args=[message.id]))
	else:
		message_form = MessageForm(instance=message)
		message_formset = MessageFormSet(instance=message)
	return render_to_response('newsletter/message.html',
		{'message': message,
		'message_form': message_form,
		'message_formset': message_formset, },
		context_instance=RequestContext(request),)

@permission_required('newsletter.add_message')
def message_archive(request):
	message_list = Message.objects.all().order_by("-date")
	return render_to_response('newsletter/messages.html',
		{'message_list': message_list,},
		context_instance=RequestContext(request),)

@permission_required('newsletter.add_subscriber')
def subscriber(request, subscriber_id):
	subscriber = get_object_or_404(Subscriber, pk=subscriber_id)
	if request.method == "POST":
		form = SubscriberForm(request.POST, instance=subscriber)
		if form.is_valid():
			form.save()
	else:
		form = SubscriberForm(instance=subscriber)
	return render_to_response('newsletter/subscriber.html',
		{'subscriber': subscriber,
		'form': form, },
		context_instance=RequestContext(request),)

def subscriber_add(request, list_id):
	list = get_object_or_404(List, pk=list_id)
	if request.method == "POST":
		form = SubscriberFormPublic(request.POST)
		if form.is_valid():
			subscriber = Subscriber(name=form.cleaned_data['name'],
				email = form.cleaned_data['email'],
				subscription = list,
				confirmed = False)
			subscriber.save()
			text = loader.render_to_string("email/newsletter_confirm.html",
				{'subscriber': subscriber,
				'site_url': settings.SITE_URL,})
			send_mail(_('Confirm subscription'), text, settings.NEWSLETTER_FROM,
				[subscriber.email], fail_silently=False)
			return HttpResponse(_('<h1>Thanks for subscribing</h1>An e-mail asking for confirmation willbe sent shortly to %s' % (subscriber.email)))
	formset = SubscriberFormPublic()
	return render_to_response('newsletter/subscriber_add.html',
		{'form': formset,
		'list': list, },
		context_instance=RequestContext(request),)

def subscriber_confirm(request, subscriber_id, token):
	subscriber = get_object_or_404(Subscriber, pk=subscriber_id)
	if subscriber.token == token:
		subscriber.confirmed = True
		subscriber.save()
		return HttpResponse(_('<h1>Subscribtion confirmed</h1>'))
	return HttpResponse(_('<h1>Couldn\'t confirm - token mismatch</h1>'))

def subscriber_public_delete(request, subscriber_id, token):
	try:
		subscriber = Subscriber.objects.get(pk=subscriber_id)
	except Subscriber.DoesNotExist:
		return HttpResponse(_('<h1>Subscribtion doesn\'t exist (anymore?)</h1>'))
	if subscriber.token == token:
		subscriber.delete()
		return HttpResponse(_('<h1>Subscribtion cancelled</h1>'))
	return HttpResponse(_('<h1>Couldn\'t cancel - token mismatch</h1>'))

@permission_required('newsletter.delete_subscriber')
def subscriber_delete(request, subscriber_id):
	subscriber = get_object_or_404(Subscriber, pk=subscriber_id)
	list = subscriber.subscription.id
	subscriber.delete()
	return HttpResponseRedirect(reverse('subscribers_list', args=[list]))

@permission_required('newsletter.add_subscriber')
def subscribers_list(request, list_id):
	list = get_object_or_404(List, pk=list_id)
	subscribers = Subscriber.objects.filter(subscription=list).order_by('email')
	return render_to_response('newsletter/subscribers.html',
		{'list': list,
		'subscribers': subscribers, },
		context_instance=RequestContext(request),)

@permission_required('newsletter.add_subscriber')
def subscribers_add(request, list_id):
	list = get_object_or_404(List, pk=list_id)
	SubscriberFormSet = inlineformset_factory(List, Subscriber, extra=10, can_delete=False)
	if request.method == "POST":
		formset = SubscriberFormSet(request.POST, instance=list)
		if formset.is_valid():
			formset.save()
			messages.success(request, _("Saved new subscribers"))
	formset = SubscriberFormSet()
	return render_to_response('newsletter/subscribers_add.html',
		{'formset': formset,
		'list': list, },
		context_instance=RequestContext(request),)

@permission_required('newsletter.add_job')
def job(request, job_id):
	job = get_object_or_404(Job, pk=job_id)
	letters = Letter.objects.filter(job=job)
	return render_to_response('newsletter/job.html',
		{'job': job,
		'letters': letters, },
		context_instance=RequestContext(request),)

@permission_required('newsletter.add_job')
def job_archive(request):
	jobs = Job.objects.all().order_by("-date")
	return render_to_response('newsletter/jobs.html',
		{'jobs': jobs,},
		context_instance=RequestContext(request),)

@permission_required('newsletter.add_job')
def job_new(request):
	if request.method == "POST":
		form = JobForm(request.POST)
		if form.is_valid():
			job = Job(message = form.cleaned_data['message'],
				to = form.cleaned_data['to'],
				sender = request.user, )
			job.save()
			job.message.locked = True
			job.message.save()
			recipients = job.to.recipients.filter(confirmed=True)
			for recipient in recipients:
				letter = Letter(job=job, recipient=recipient)
				letter.save()
			messages.success(request, _("Queued %s Newsletters for delivery." % (recipients.count())))
			return HttpResponseRedirect(reverse('job', args=[job.id]))
	else:
		form = JobForm()
	return render_to_response('newsletter/job_new.html',
		{'form': form, },
		context_instance=RequestContext(request),)
