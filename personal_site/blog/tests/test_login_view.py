from django.test import TestCase, Client
from blog.models import BlogUser
from django.urls import reverse, resolve
from blog.views import login

class TestLoginView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = BlogUser.objects.create_user(email='test@test.test', password='password')

    def test_login_url_resolves_login_view(self):
        view = resolve(reverse('blog:login'))
        self.assertEqual(view.func, login)
    
    def test_login_view_template(self):
        response = self.client.get(reverse('blog:login'))
        self.assertTemplateUsed(response, 'blog/login.html')
        self.assertContains(response, '<!-- This is line for testing purposes. TEMPLATE: login.html -->')

    def test_login(self):
        response = self.client.post(reverse('blog:login'), {'email': 'test@test.test', 'password': 'password'})
        self.assertRedirects(response, reverse('blog:home'))
        self.assertTrue(self.client.session['_auth_user_id'])

    def test_invalid_login(self):
        response = self.client.post(reverse('blog:login'), {'email': 'random@random.test', 'password': 'random'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.client.session.get('_auth_user_id'))
        self.assertContains(response, '<!-- This is line for testing purposes. TEMPLATE: login.html -->')
        self.assertContains(response, 'Invalid email or password')
