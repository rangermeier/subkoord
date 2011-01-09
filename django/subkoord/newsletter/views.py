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
from django.utils import simplejson
from datetime import date, datetime
from models import *
from forms import *
from mailbox_utils import *

@permission_required('newsletter.add_subscriber')
def index(request):
	message_list = Message.objects.order_by('-date')[:7]
	subscribers = Subscriber.objects.all().order_by('-date')[:10]
	lists = List.objects.all()
	return render_to_response('newsletter/index.html',
		{'message_list': message_list,
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
	job_form = JobMessageForm(initial = {'message': message.id,})
	preview_form = PreviewMessageForm(initial = {'message': message.id,})
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
		'preview_form': preview_form,
		'message_form': message_form,
		'message_formset': message_formset,
		'job_form': job_form,},
		context_instance=RequestContext(request),)

#@permission_required('newsletter.add_message')
#def message_preview(request, message_id):
#	if request.method == "POST":
#		message = get_object_or_404(Message, pk=message_id)
#		form = PreviewMessageForm(request.POST)
#		if form.is_valid():
#			for recipient in form.cleaned_data["to"]:
#				letter = Letter()
#	return HttpResponseRedirect(reverse('message', args=[message_id]))

@permission_required('newsletter.add_message')
def message_archive(request):
	message_list = Message.objects.all().order_by("-date")
	return render_to_response('newsletter/messages.html',
		{'message_list': message_list,},
		context_instance=RequestContext(request),)

@permission_required('newsletter.add_job')
def job(request, job_id):
	job = get_object_or_404(Job, pk=job_id)
	return render_to_response('newsletter/job.html',
		{'job': job, },
		context_instance=RequestContext(request),)

@permission_required('newsletter.add_job')
def job_new(request, preview_send=False, **kwargs):
	if request.method == "POST":
		form = JobForm(request.POST)
		if form.is_valid():
			job = Job(message = form.cleaned_data['message'],
				to = form.cleaned_data['to'],
				sender = request.user, letters_sent = 0)
			job.save()
			if preview_send:
				for letter in job.letters.all():
					letter.send()
					letter.delete()
				print "job count: %s" % (job.message.jobs.count())
				if job.message.jobs.count() == 1:
					job.message.locked = False
					job.message.save()
				messages.success(request, _("Sent Preview to list %s." % (job.to.name)))
				job.delete()
				return HttpResponseRedirect(reverse('message', args=[form.cleaned_data['message'].id]))
			messages.success(request, _("Queued %s Newsletters for delivery." % (job.letters_total-job.letters_sent)))
			return HttpResponseRedirect(reverse('job', args=[job.id]))
	else:
		form = JobForm()
	return render_to_response('newsletter/job_new.html',
		{'form': form, },
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
	json = simplejson.dumps({'subscriber_id':subscriber_id,
		'email': subscriber.email})
	subscriber.delete()
	if request.is_ajax():
		return HttpResponse(json, mimetype='application/json',)
	return HttpResponseRedirect(reverse('subscribers_list', args=[list]))

@permission_required('newsletter.delete_subscriber')
def subscribers_delete(request, subscribers_ids):
	ids = subscribers_ids.split(",")
	subscribers = Subscriber.objects.filter(id__in=ids)
	messages.success(request, _("Deleted %s subscribers" % (len(subscribers))))
	for subscriber in subscribers:
		subscriber.delete()
	return HttpResponseRedirect(reverse('newsletter_index'))

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
	else: formset = SubscriberFormSet()
	return render_to_response('newsletter/subscribers_add.html',
		{'formset': formset,
		'list': list, },
		context_instance=RequestContext(request),)

@permission_required('newsletter.delete_subscriber')
def empty_error_mailbox(request):
	server = get_server()
	messagesInfo = server.list()[1]
	for msg in messagesInfo:
		msgNum = msg.split(" ")[0]
		server.dele(msgNum)
	server.quit()
	messages.success(request, _("Removed all messages from error mailbox"))
	return HttpResponseRedirect(reverse('newsletter_index'))

@permission_required('newsletter.delete_subscriber')
def error_mailbox(request):
	server = get_server()
	messagesInfo = server.list()[1]
	mails = []
	subscribers_ids = []
	for msg in messagesInfo:
		msgNum = msg.split(" ")[0]
		full_message = "\n".join(server.retr(msgNum)[1])
		mail = parse_email(full_message)
		mail['subscriber'] = match_error_to_subscriber(mail)
		if mail['subscriber']:
			subscribers_ids.append(u'%s' % (mail['subscriber'].id))
		mails.append(mail)
	server.quit()
	return render_to_response('newsletter/error_mailbox.html',
		{'mails': mails,
		'all_subscribers_ids': ",".join(subscribers_ids), },
		context_instance=RequestContext(request),)
