from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from models import *


class WikiTest(TestCase):
    fixtures = ['test_auth.json', 'test_wiki.json', ]
    def setUp(self):
        self.client = Client()
        self.client.login(username='test' , password='test')

    def test_client_login(self):
        self.client.logout()
        r = self.client.get('/wiki/', {})
        self.assertEqual(r.status_code, 302)
        self.client.login(username='test', password='test')
        r = self.client.get('/wiki/', {})
        self.assertContains(r, "<a href=\"/wiki/Test-Page/\">", 1, 200)
        r = self.client.get('/', {})
        self.assertContains(r, "<a href=\"/wiki/\">")

    def create_article(self, title):
        return self.client.post(
            "/wiki/%s/edit/" % title, {
                'title': title,
                'content_html': "this is a new [[wiki]] article on [[%s]]" % title,
                'category': 1, })
                #'attachments-TOTAL_FORMS': 1,
                #'attachments-INITIAL_FORMS': 1,
                #'attachments-0-id': 1,
                #'attachments-0-file': "", })

    def test_wiki_redirecting(self):
        self.client.login(username='test' , password='test')
        r = self.client.get('/wiki/bar/', {})
        self.assertEquals(r.status_code, 302)
        r = self.client.get('/wiki/bar/edit/', {})

    def test_wiki_create(self):
        # creating an article
        r = self.create_article("bar")
        r = self.client.get('/wiki/bar/', {})
        self.assertContains(r, "this is a new <a href=\"/wiki/wiki/\" class=\"new_page\">wiki</a> article on <a href=\"/wiki/bar/\" class=\"\">bar</a>",
            1, 200)

    def test_wiki_rename(self):
        # renaming the article
        r = self.create_article("bar")
        r = self.client.post("/wiki/bar/edit/", {'title': 'foo',
            'content_html': 'this is a new [[wiki]] article on [[bar]]',
            'category': 1})
        r = self.client.get('/wiki/foo/', {})
        self.assertEquals(r.status_code, 200)
        r = self.client.get('/wiki/bar/', {})
        self.assertEquals(r.status_code, 302)

    def test_wiki_index(self):
        # the wiki-index has a link to the new page
        r = self.create_article("bar")
        r = self.client.get('/wiki/', {})
        self.assertContains(r, "<a href=\"/wiki/bar/\">")

    def test_wiki_delete(self):
        # deleting the article
        r = self.create_article("foo")
        r = self.client.post("/wiki/foo/delete/", {'really_sure': 'yes'})
        r = self.client.get('/wiki/foo/', {})
        self.assertEquals(r.status_code, 302)

    def test_wiki_delete2(self):
        # deleting an non-existant article
        r = self.client.post("/wiki/bar/delete/", {'really_sure': 'yes'})
        self.assertEquals(r.status_code, 404)
