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
		self.assertEqual(len(r.context['user_list']), 4)
		self.assertTemplateUsed(r,  "users/user_list.html")

		r = self.client.get('/user/1/', {})
		self.assertEqual(r.status_code, 200)
		self.assertEqual(r.context['usr'].pk, 1)
		self.assertTemplateUsed(r, "users/user.html")

		r = self.client.get('/user/99/', {})
		self.assertEqual(r.status_code, 404)

		r = self.client.get('/user/password/', {})
		self.assertEqual(r.status_code, 200)
		self.assertTemplateUsed(r,  "users/user_edit.html")
