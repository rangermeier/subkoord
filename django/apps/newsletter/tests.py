from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.utils.html import escape
from models import *

NEWSLETTER_USER = 'letterman'

class NewsletterTest(TestCase):
    fixtures = ['test_auth.json', 'test_newsletter.json', ]
    def setUp(self):
        self.client = Client()

    def test_client_login(self):
        r = self.client.get('/newsletter/', {})
        self.assertEqual(r.status_code, 302)
        self.client.login(username='test', password='test')
        r = self.client.get('/newsletter/', {})
        self.assertEqual(r.status_code, 302)
        self.client.logout()
        self.client.login(username=NEWSLETTER_USER , password='test')
        r = self.client.get('/newsletter/', {})
        self.assertEqual(r.status_code, 200)
        r = self.client.get('/', {})
        self.assertContains(r, "<a href=\"/newsletter/\">", 1, 200)

    def test_client_index(self):
        self.client.login(username=NEWSLETTER_USER , password='test')
        r = self.client.get('/newsletter/', {})
        self.assertEqual(len(r.context['subscribers']), 5)
        self.assertContains(r, "<a href=\"/newsletter/compose/\">")
        self.assertTemplateUsed(r,  "newsletter/index.html")

    def test_client_message(self):
        self.client.login(username=NEWSLETTER_USER , password='test')
        r = self.client.get('/newsletter/compose/', {})
        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, "newsletter/message.html")

        r = self.client.get('/newsletter/message/1/', {})
        self.assertContains(r, "<a href=\"/newsletter/job/1/\">", 1, 200)
        self.assertContains(r, "<form action=\"/newsletter/send/", 1)
        self.assertNotContains(r, "<form action=\"/newsletter/message/1/\"",)
        self.assertEqual(r.context['message'].pk, 1)
        self.assertTemplateUsed(r, "newsletter/message.html")

        r = self.client.get('/newsletter/message/2/', {})
        self.assertNotContains(r, "<a href=\"/newsletter/job/", 200)
        self.assertContains(r, "<form action=\"/newsletter/send/", 1)
        self.assertContains(r, "<form action=\"/newsletter/message/2/\"", 1,)
        self.assertTemplateUsed(r, "newsletter/message.html")

        r = self.client.get('/newsletter/message/99/', {})
        self.assertEqual(r.status_code, 404)

    def test_client_list(self):
        self.client.login(username=NEWSLETTER_USER , password='test')
        r = self.client.get('/newsletter/mailinglist/1/', {})
        self.assertContains(r, "<a href=\"/newsletter/mailinglist/1/add/\">",)
        self.assertContains(r, "<a href=\"/newsletter/mailinglist/1/subscribe/", )
        self.assertTemplateUsed(r, "newsletter/subscribers.html")

        r = self.client.get('/newsletter/mailinglist/1/add/', {})
        self.assertContains(r, "<input id=\"id_recipients-0-email\"", 1, 200)
        self.assertContains(r, "<input id=\"id_recipients-9-email\"", 1, 200)
        self.assertTemplateUsed(r, "newsletter/subscribers_add.html")

        r = self.client.get('/newsletter/subscriber/1/', {})
        self.assertContains(r, "name=\"email\" ", 1, 200)
        self.assertTemplateUsed(r, "newsletter/subscriber.html")

    def test_model_subscriber(self):
        subscriber = Subscriber.objects.get(pk=1)
        self.assertEqual(subscriber.email, "test@example.com")
        self.assertTrue(subscriber.confirmed,)

        subscriber = Subscriber(email="foo@bar.org", name="Foo Bar")
        subscriber.save()
        self.assertTrue(subscriber.confirmed)

        r = self.client.post(reverse("subscriber_add", args=[1]), {'email':"publicsubscriber@bar.org", 'name':"Puh Bar"})
        self.assertContains(r, _("Thanks for subscribing!"), 1, 200)
        subscriber = Subscriber.objects.get(email__exact="publicsubscriber@bar.org")
        self.assertFalse(subscriber.confirmed)
        r = self.client.get('newsletter/confirm/%s/abcd/' % (subscriber.id))
        self.assertEqual(r.status_code, 404)
        r = self.client.get(reverse("subscriber_confirm", args=[subscriber.id, "1234567890ab"]))
        self.assertContains(r, escape(_("Couldn't confirm - token mismatch")), 1, 200)
        r = self.client.get(reverse("subscriber_confirm", args=[subscriber.id, subscriber.token]))
        self.assertContains(r, _("Subscribtion confirmed"), 1, 200)
        subscriber = Subscriber.objects.get(email__exact="publicsubscriber@bar.org")
        self.assertTrue(subscriber.confirmed)
        del_url = reverse("subscriber_public_delete", args=[subscriber.id, subscriber.token])
        r = self.client.get(del_url)
        self.assertContains(r , "action=\"%s\" method=\"post" % del_url, 1, 200)
        self.assertContains(r , "type=\"submit", 1, 200)
        r = self.client.post(reverse("subscriber_public_delete", args=[subscriber.id, subscriber.token]))
        self.assertContains(r , _("Subscribtion cancelled"), 1, 200)
        subscriber_count = Subscriber.objects.filter(email__exact="publicsubscriber@bar.org").count()
        self.assertEqual(subscriber_count, 0)
