from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from models import *


class WikiTest(TestCase):
	fixtures = ['test.yaml']
	def setUp(self):
		self.client = Client()

	def test_client_login(self):
		r = self.client.get('/wiki/', {})
		self.assertEqual(r.status_code, 302)
		self.client.login(username='test', password='test')
		r = self.client.get('/wiki/', {})
		self.assertContains(r, "<a href=\"/wiki/Test-Page/\">", 1, 200)
		r = self.client.get('/', {})
		self.assertContains(r, "<a href=\"/wiki/\">")


	def test_wiki(self):
		self.client.login(username='test' , password='test')
		r = self.client.get('/wiki/bar/', {})
		self.assertEquals(r.status_code, 302)
		r = self.client.get('/wiki/bar/edit/', {})
		# creating an article
		self.assertContains(r, "<form action=\"/wiki/bar/edit/\"", 1, 200)
		r = self.client.post("/wiki/bar/edit/", {'title': 'bar',
			'content': 'this is a new [[wiki]] article on [[bar]]',
			'category': 1,
			#'attachments-TOTAL_FORMS': 1,
			#'attachments-INITIAL_FORMS': 1,
			#'attachments-0-id': 1,
			#'attachments-0-file': "",
			})
		r = self.client.get('/wiki/bar/', {})
		self.assertContains(r, "this is a new <a href=\"/wiki/wiki/\" class=\"new_page\">wiki</a> article on <a href=\"/wiki/bar/\" class=\"\">bar</a>",
			1, 200)
		# renaming the article
		r = self.client.post("/wiki/bar/edit/", {'title': 'foo',
			'content': 'this is a new [[wiki]] article on [[bar]]',
			'category': 1})
		r = self.client.get('/wiki/foo/', {})
		self.assertEquals(r.status_code, 200)
		r = self.client.get('/wiki/bar/', {})
		self.assertEquals(r.status_code, 302)
		# the wiki-index has a link to the new page
		r = self.client.get('/wiki/', {})
		self.assertContains(r, "<a href=\"/wiki/foo/\">")
		# deleting the article
		r = self.client.post("/wiki/bar/delete/", {'really_sure': 'yes'})
		r = self.client.post("/wiki/foo/delete/", {'really_sure': 'yes'})
		r = self.client.get('/wiki/foo/', {})
		self.assertEquals(r.status_code, 302)
		# deleting an non-existant article
		r = self.client.post("/wiki/bar/delete/", {'really_sure': 'yes'})
		self.assertEquals(r.status_code, 404)
