from django.test import TestCase, Client
from django.urls import reverse, resolve
from blog.models import BlogUser, BlogPost, Category, HistoryLog
from blog.views import categories_admin


class TestCategoriesAdmin(TestCase):
    def setUp(self):
        self.user = BlogUser.objects.create_user(email='test@test.test', password='test')
        self.client = Client()
        self.client.force_login(self.user)

    def test_categories_admin_resolves(self):
        response = self.client.get(reverse('blog:categories_admin'))
        self.assertEqual(response.status_code, 200)
    
    def test_categories_admin_template(self):
        response = self.client.get(reverse('blog:categories_admin'))
        self.assertContains(response, '<!-- This is line for testing purposes. TEMPLATE: categories_admin.html -->')
        self.assertTemplateUsed(response, 'blog/categories_admin.html')
    
    def test_categories_admin_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('blog:categories_admin'))
        self.assertRedirects(response, f'{reverse('blog:login')}?next={reverse("blog:categories_admin")}')
    
