from django.test import TestCase, Client
from django.urls import reverse, resolve
from blog.views import home


class TestHomeView(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_home_url_resolves(self):
        url = reverse('blog:home')
        self.assertEqual(resolve(url).func, home)

    def test_home_view(self):
        response = self.client.get(reverse('blog:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')
    
    def test_home_view_template(self):
        response = self.client.get(reverse('blog:home'))
        self.assertTemplateUsed(response, 'blog/home.html')
        self.assertContains(response, '<!-- This is line for testing purposes. TEMPLATE: home.html -->')