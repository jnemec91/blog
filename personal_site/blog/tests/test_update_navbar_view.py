from django.test import TestCase, Client
from django.urls import reverse, resolve
from blog.views import update_navbar


class Testupdate_navbarView(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_update_navbar_url_resolves(self):
        url = reverse('blog:update_navbar')
        self.assertEqual(resolve(url).func, update_navbar)

    def test_update_navbar_view(self):
        response = self.client.get(reverse('blog:update_navbar'))
        self.assertEqual(response.status_code, 200)
    
    def test_update_navbar_view_template(self):
        response = self.client.get(reverse('blog:update_navbar'))
        self.assertTemplateUsed(response, 'blog/components/navbar.html')
        self.assertContains(response, '<!-- This is line for testing purposes. TEMPLATE: navbar.html -->')