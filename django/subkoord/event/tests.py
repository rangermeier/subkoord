from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from models import *

EVENT_USER = "partyman"

class EventTest(TestCase):
	fixtures = ['test.json']
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


	def test_urls(self):
		self.client.login(username=EVENT_USER , password='test')
		r = self.client.get('/event/1/', {})
		self.assertContains(r, "schwer experimentell!", 1, 200)
		r = self.client.get('/event/1/edit/', {})
		self.assertContains(r, "<form action=\"/event/1/edit/\" method=\"post", 1, 200)

	def test_jobs(self):
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


__test__ = {"doctest": """

>>> e = Event.objects.get(pk = 1)
>>> e
<Event: The rocking Testers>
>>> e.tasks
[<Task: Koordination>, <Task: Fruehdienst>, <Task: Spaetdienst>]
>>> e.jobs
[]
>>> e.all_tasks_satisfied
False
>>> t = e.tasks[0]
>>> t.satisfied(e)
False
>>> t.maxed_out(e)
False

>>> u = User.objects.get(username = 'partyman')
>>> j1 = Job(event=e, user=u, task=t)
>>> j1
<Job: The rocking Testers - Koordination: partyman>
>>> e.jobs
[]
>>> j1.save()
>>> e.jobs
[<Job: The rocking Testers - Koordination: partyman>]
>>> t.satisfied(e)
True
>>> t.maxed_out(e)
True
>>> j2 = Job(event = e, user=u, task=e.tasks[1])
>>> j2.save()
>>> e.tasks[1].satisfied(e)
False
>>> e.tasks[1].maxed_out(e)
False
>>> j3 = Job(event = e, user=u, task=e.tasks[2])
>>> j3.save()
>>> u1 = User.objects.get(username = 'susi')
>>> j4 = Job(event = e, user=u1, task=e.tasks[1])
>>> j4.save()
>>> e.all_tasks_satisfied
False
>>> e.tasks[1].satisfied(e)
True
>>> e.tasks[1].maxed_out(e)
False
>>> j5 = Job(event = e, user=u1, task=e.tasks[2])
>>> j5.save()
>>> e.all_tasks_satisfied
True
>>> e.jobs
[<Job: The rocking Testers - Koordination: partyman>, <Job: The rocking Testers - Fruehdienst: partyman>, <Job: The rocking Testers - Spaetdienst: partyman>, <Job: The rocking Testers - Fruehdienst: susi>, <Job: The rocking Testers - Spaetdienst: susi>]
>>> j2.delete()
>>> e.all_tasks_satisfied
False
"""}
