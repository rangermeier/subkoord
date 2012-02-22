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
from subkoord.attachment.forms import attachment_formset_handler
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
    message = get_object_or_404(Message, pk=message_id)
    job_form = JobMessageForm(initial = {'message': message.id,})
    preview_form = PreviewMessageForm(initial = {'message': message.id,})
    attachment_formset = attachment_formset_handler(request, message)
    if not message.locked and request.method == "POST":
        message_form = MessageForm(request.POST, instance=message)
        if message_form.is_valid() and attachment_formset.is_valid():
            message_form.save()
            return HttpResponseRedirect(reverse('message', args=[message.id]))
    else:
        message_form = MessageForm(instance=message)
    return render_to_response('newsletter/message.html',
        {'message': message,
        'preview_form': preview_form,
        'message_form': message_form,
        'attachment_formset': attachment_formset,
        'job_form': job_form,},
        context_instance=RequestContext(request),)


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
            send_mail(_('Confirm subscription'), text, list.from_address,
                [subscriber.email], fail_silently=False)
            heading = _('Thanks for subscribing!')
            message = _('An e-mail asking for confirmation will be sent shortly to %s' % (subscriber.email))
            return render_to_response('newsletter/subscriber_public_message.html',
                {'heading': heading,
                'message': message, },
                context_instance=RequestContext(request),)
    else: form = SubscriberFormPublic()
    return render_to_response('newsletter/subscriber_add.html',
        {'form': form,
        'list': list, },
        context_instance=RequestContext(request),)

def subscriber_confirm(request, subscriber_id, token):
    subscriber = get_object_or_404(Subscriber, pk=subscriber_id)
    if subscriber.confirmed:
        heading = _('Already confirmed')
    elif subscriber.token == token:
        subscriber.confirmed = True
        subscriber.save()
        heading =_('Subscribtion confirmed')
    else: heading = _('Couldn\'t confirm - token mismatch')
    return render_to_response('newsletter/subscriber_public_message.html',
        {'heading': heading,  },
        context_instance=RequestContext(request),)

def subscriber_public_delete(request, subscriber_id, token):
    try:
        subscriber = Subscriber.objects.get(pk=subscriber_id)
    except Subscriber.DoesNotExist:
        return render_to_response('newsletter/subscriber_public_message.html',
            {'heading': _('Subscribtion doesn\'t exist (anymore?)'),  },
            context_instance=RequestContext(request),)
    if subscriber.token != token:
        heading = _('Couldn\'t cancel - token mismatch')
    elif request.method != "POST":
        return render_to_response('newsletter/subscription_delete.html',
            {'subscriber': subscriber,
            'token': token, },
            context_instance=RequestContext(request),)
    else:
        subscriber.delete()
        heading = _('Subscribtion cancelled')
    return render_to_response('newsletter/subscriber_public_message.html',
        {'heading': heading,  },
        context_instance=RequestContext(request),)

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
    unassigned_mails = []
    assigned_mails = []
    subscribers_ids = []
    for msg in messagesInfo:
        msgNum = msg.split(" ")[0]
        full_message = "\n".join(server.retr(msgNum)[1])
        mail = parse_email(full_message)
        mail['msg_num'] = msgNum
        mail['subscriber'] = match_error_to_subscriber(mail)
        if mail['subscriber']:
            mail['subscriber_id'] = mail['subscriber'].id
            subscribers_ids.append(u'%s' % (mail['subscriber'].id))
            assigned_mails.append(mail)
        else: unassigned_mails.append(mail)
    server.quit()
    return render_to_response('newsletter/error_mailbox.html',
        {'unassigned_mails': unassigned_mails,
        'assigned_mails': assigned_mails,
        'all_subscribers_ids': ",".join(subscribers_ids), },
        context_instance=RequestContext(request),)

@permission_required('newsletter.delete_subscriber')
def delete_error_mail(request, msg_id):
    server = get_server()
    messagesInfo = server.list()[1]
    for msg in messagesInfo:
        msgNum = msg.split(" ")[0]
        if msgNum == msg_id:
            server.dele(msgNum)
    server.quit()
    messages.success(request, _("Removed message from error mailbox"))
    return HttpResponseRedirect(reverse('error_mailbox'))

@permission_required('newsletter.delete_subscriber')
def delete_unassigned_mails(request):
    server = get_server()
    messagesInfo = server.list()[1]
    for msg in messagesInfo:
        msgNum = msg.split(" ")[0]
        full_message = "\n".join(server.retr(msgNum)[1])
        mail = parse_email(full_message)
        subscriber = match_error_to_subscriber(mail)
        if not subscriber:
            server.dele(msgNum)
    server.quit()
    messages.success(request, _("Removed unassigned messages from error mailbox"))
    return HttpResponseRedirect(reverse('error_mailbox'))
