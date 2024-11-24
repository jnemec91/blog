from django.test import TestCase, Client
from blog.models import BlogUser
from django.urls import reverse, resolve
from blog.views import logout
from django.contrib.auth import login as auth_login

class TestLogoutView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = BlogUser.objects.create_user(email='test@test.test', password='password')
        self.client.post(reverse('blog:login'), {'email': 'test@test.test', 'password': 'password'})
    
    def test_logout_url_resolves_logout_view(self):
        view = resolve(reverse('blog:logout'))
        self.assertEqual(view.func, logout)

    def test_logout(self):
        response = self.client.get(reverse('blog:logout'))
        self.assertRedirects(response, reverse('blog:home'))
        self.assertFalse(self.client.session.get('_auth_user_id'))
    
    def test_logout_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('blog:logout'))
        self.assertRedirects(response, f'{reverse('blog:login')}?next={reverse("blog:logout")}')
        self.assertFalse(self.client.session.get('_auth_user_id'))