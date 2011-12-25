from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_change

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
