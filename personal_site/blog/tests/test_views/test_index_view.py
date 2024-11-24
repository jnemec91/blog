from django.test import TestCase, Client
from django.urls import reverse, resolve
from blog.views import index


class TestIndexView(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_index_url_resolves(self):
        url = reverse('blog:index')
        self.assertEqual(resolve(url).func, index)

    def test_index_view(self):
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
    
    def test_index_view_template(self):
        response = self.client.get(reverse('blog:index'))
        self.assertTemplateUsed(response, 'blog/index.html')
        self.assertContains(response, '<!-- This is line for testing purposes. TEMPLATE: index.html -->')