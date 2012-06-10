from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_change
from django.db.models import Min
from copy import deepcopy
import datetime
from event.models import Job, Task, Event

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

@login_required
def user_list(request):
    user_list = User.objects.all().order_by('username')
    return render_to_response('users/user_list.html',
        {'user_list': user_list },
        context_instance=RequestContext(request),)

@login_required
def user_view(request, user_id):
    usr = get_object_or_404(User, id=user_id)
    return render_to_response('users/user.html',
        {'usr': usr },
        context_instance=RequestContext(request),)

@login_required
def user_change_password(request):
    return password_change(request, 'users/user_edit.html',
        reverse('user_view', args=[request.user.id]))

@login_required
def user_statistics(request, year=None):
    user_list = User.objects.all().order_by('username')
    tasks = Task.objects.all()
    first_event = Event.objects.all().aggregate(Min("date"))
    if year:
        inner_qs = Event.objects.filter(date__year=year)
        jobs = Job.objects.filter(event__in=inner_qs)
    else:
        jobs = Job.objects.all()
    for user in user_list:
        user.stats = deepcopy(tasks)
        user.stats.sum = 0
        for task in user.stats:
            task.count = 0
            for job in jobs:
                if job.user == user and job.task == task:
                    task.count += 1
                    user.stats.sum += 1
    return render_to_response('users/user_statistics.html',
        {'user_list': user_list,
        'tasks': tasks,
        'year': year,
        'years': range(first_event["date__min"].year, datetime.datetime.today().year+1), },
        context_instance=RequestContext(request),)
