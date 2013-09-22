from django.test import TestCase
from django.test import Client

class UserTest(TestCase):
    fixtures = ['test_auth.json', 'test_event.json', ]
    def setUp(self):
        self.client = Client()
        self.client.login(username='test', password='test')

    def test_client_login(self):
        self.client.logout()
        r = self.client.get('/user/', {})
        self.assertEqual(r.status_code, 302)
        self.client.login(username='test', password='test')
        r = self.client.get('/user/', {})
        self.assertEqual(r.status_code, 200)

    def test_client_user_list(self):
        r = self.client.get('/user/', {})
        self.assertEqual(len(r.context['user_list']), 6)
        self.assertTemplateUsed(r,  "users/user_list.html")

    def test_client_user_single(self):
        r = self.client.get('/user/1/', {})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['usr'].pk, 1)
        self.assertTemplateUsed(r, "users/user.html")

    def test_client_user_jobs(self):
        r = self.client.get('/user/1/', {})
        self.assertEqual(len(r.context['usr'].jobs.all()), 1)
        self.assertEqual(r.context['usr'].jobs.all()[0].event.id, 3)

    def test_client_user_non_existant(self):
        r = self.client.get('/user/99/', {})
        self.assertEqual(r.status_code, 404)

    def test_client_user_password_form(self):
        r = self.client.get('/user/password/', {})
        self.assertContains(r, "<form action=\"/user/password/\" method=\"POST", 1, 200)
        self.assertTemplateUsed(r,  "users/user_edit.html")

    def test_client_password_change(self):
        r = self.client.post('/user/password/', {'old_password': 'test',
            'new_password1': 'newpassword', 'new_password2': 'newpassword'})
        self.client.logout()
        r = self.client.get('/user/', {})
        self.assertEqual(r.status_code, 302)
        self.client.login(username='test', password='newpassword')
        r = self.client.get('/user/', {})
        self.assertEqual(r.status_code, 200)
