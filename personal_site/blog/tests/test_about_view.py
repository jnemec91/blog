from django.test import TestCase, Client
from django.urls import reverse, resolve
from blog.views import about


class TestaboutView(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_about_url_resolves(self):
        url = reverse('blog:about')
        self.assertEqual(resolve(url).func, about)

    def test_about_view(self):
        response = self.client.get(reverse('blog:about'))
        self.assertEqual(response.status_code, 200)
    
    def test_about_view_template(self):
        response = self.client.get(reverse('blog:about'))
        self.assertTemplateUsed(response, 'blog/about.html')
        self.assertContains(response, '<!-- This is line for testing purposes. TEMPLATE: about.html -->')