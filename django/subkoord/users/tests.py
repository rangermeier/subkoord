from django.test import TestCase
from django.test import Client

class UserTest(TestCase):
	fixtures = ['test.json']
	def setUp(self):
		self.client = Client()

	def test_client_login(self):
		r = self.client.get('/user/', {})
		self.assertEqual(r.status_code, 302)
		self.client.login(username='test', password='test')
		r = self.client.get('/user/', {})
		self.assertEqual(r.status_code, 200)

	def test_client_user(self):
		self.client.login(username='test', password='test')
		r = self.client.get('/user/', {})
		self.assertEqual(len(r.context['user_list']), 5)
		self.assertTemplateUsed(r,  "users/user_list.html")

		r = self.client.get('/user/1/', {})
		self.assertEqual(r.status_code, 200)
		self.assertEqual(r.context['usr'].pk, 1)
		self.assertEqual(len(r.context['usr'].jobs.all()), 1)
		self.assertEqual(r.context['usr'].jobs.all()[0].event.id, 3)
		self.assertTemplateUsed(r, "users/user.html")

		r = self.client.get('/user/99/', {})
		self.assertEqual(r.status_code, 404)

		r = self.client.get('/user/password/', {})
		self.assertContains(r, "<form action=\"/user/password/\" method=\"POST", 1, 200)
		self.assertTemplateUsed(r,  "users/user_edit.html")


	def test_client_password_change(self):
		self.client.login(username='test', password='test')
		r = self.client.post('/user/password/', {'old_password': 'test',
			'new_password1': 'newpassword', 'new_password2': 'newpassword'})
		self.client.logout()
		r = self.client.get('/user/', {})
		self.assertEqual(r.status_code, 302)
		self.client.login(username='test', password='newpassword')
		r = self.client.get('/user/', {})
		self.assertEqual(r.status_code, 200)
