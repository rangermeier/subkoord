from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.markup.templatetags.markup import textile
from django.utils.translation import ugettext as _
from subkoord.wiki.models import Wikipage, WikipageForm
from subkoord.wiki.templatetags.wikitags import *

@login_required
def index(request):
	"""Return simple list of wiki pages"""
	pages = Wikipage.objects.all().order_by('category', '-last_changed')
	return render_to_response('wiki/home.html',
		{'pages': pages},
		   context_instance=RequestContext(request),)

@login_required
def page(request, title):
	"""Display page, or redirect to root if page doesn't exist yet"""
	try:
		page = Wikipage.objects.get(title__exact=title)
		return render_to_response('wiki/page.html',
			{'page': page},
				context_instance=RequestContext(request),)
	except Wikipage.DoesNotExist:
		return HttpResponseRedirect(reverse('wiki_edit', args=[title]))

@login_required
def edit(request, title = None):
	"""Process submitted page edits (POST) or display editing form (GET)"""
	try:
		page = Wikipage.objects.get(title__exact=title)
		page.author = request.user
	except Wikipage.DoesNotExist:
		# Must be a new one; let's create it
		page = Wikipage(title=title, author=request.user)
	if request.POST:
		form = WikipageForm(request.POST, instance=page)
		if form.is_valid():
			form.save()
			page.content_html = textile(wikify(page.content))
			page.save()
			return HttpResponseRedirect(reverse('wiki_page', args=[page.title]))
	else:
		form = WikipageForm(instance=page)
	return render_to_response('wiki/edit.html',
		{'form': form,
		'page': page},
		context_instance=RequestContext(request),)

@login_required
def delete(request, title):
	"""Delete a page"""
	if request.POST:
		try:
			page = Wikipage.objects.get(title__exact=title)
		except Wikipage.DoesNotExist:
			return HttpResponseRedirect("/wiki/DeleteFailed/")
		page.delete()
	return HttpResponseRedirect(reverse('wiki_index'))