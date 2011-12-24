from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from models import *

EVENT_USER = "partyman"

class EventTest(TestCase):
    fixtures = ['test.yaml']
    def setUp(self):
        self.client = Client()

    def test_client_login(self):
        r = self.client.get('/event/', {})
        self.assertEqual(r.status_code, 302)
        self.client.login(username='foo', password='bar')
        r = self.client.get('/event/', {})
        self.assertEqual(r.status_code, 302)
        r = self.client.get('/event/1/', {})
        self.assertEqual(r.status_code, 302)
        self.client.login(username=EVENT_USER , password='test')
        r = self.client.get('/event/', {})
        self.assertEqual(r.status_code, 200)
        r = self.client.get('/', {})
        self.assertContains(r, "<a href=\"/event/\">", 1, 200)


    def test_cliebnt_urls(self):
        self.client.login(username=EVENT_USER , password='test')
        r = self.client.get('/event/1/', {})
        self.assertContains(r, "schwer experimentell!", 1, 200)
        r = self.client.get('/event/1/edit/', {})
        self.assertContains(r, "<form action=\"/event/1/edit/\" method=\"post", 1, 200)

    def test_client_jobs(self):
        self.client.login(username=EVENT_USER , password='test')
        r = self.client.get('/event/1/', {})
        self.assertEqual(len(r.context["event"].jobs), 0)
        # take job
        r = self.client.get('/event/1/task/1/', {})
        r = self.client.get('/event/1/', {})
        self.assertEqual(len(r.context["event"].jobs), 1)
        # cancel job
        r = self.client.get('/event/1/job/6/delete', {})
        r = self.client.get('/event/1/', {})
        self.assertEqual(len(r.context["event"].jobs), 0)

    def test_model_properties(self):
        # event properties
        e = Event.objects.get(pk = 1)
        self.assertEqual(len(e.tasks), 3)
        self.assertEqual(len(e.jobs), 0)
        self.assertTrue(not e.all_tasks_satisfied)
        # tasks
        t = e.tasks[0]
        self.assertTrue(not t.satisfied(e))
        self.assertTrue(not t.maxed_out(e))

        u = User.objects.get(username = 'partyman')
        j1 = Job(event=e, user=u, task=t)
        self.assertEqual(len(e.jobs), 0)
        j1.save()
        self.assertEqual(len(e.jobs), 1)
        self.assertTrue(t.satisfied(e))
        self.assertTrue(t.maxed_out(e))
        j2 = Job(event = e, user=u, task=e.tasks[1])
        j2.save()
        self.assertTrue(not e.tasks[1].satisfied(e))
        self.assertTrue(not e.tasks[1].maxed_out(e))
        j3 = Job(event = e, user=u, task=e.tasks[2])
        j3.save()
        u1 = User.objects.get(username = 'susi')
        j4 = Job(event = e, user=u1, task=e.tasks[1])
        j4.save()
        j5 = Job(event = e, user=u1, task=e.tasks[2])
        j5.save()
        self.assertTrue(e.all_tasks_satisfied)
        self.assertEqual(len(e.jobs), 5)
        j2.delete()
        self.assertTrue(not e.all_tasks_satisfied)


#__test__ = {"doctest": """
#"""}
