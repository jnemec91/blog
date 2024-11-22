from django.test import TestCase, Client
from django.urls import reverse, resolve
from blog.models import BlogUser, BlogPost, Category, HistoryLog
from blog.views import get_categories_table_part


class TestGetCategoriesTablePart(TestCase):
    def setUp(self):
        self.user = BlogUser.objects.create_user(email='test@test.test', password='test')
        self.category = Category.objects.create(name='test', description='test')
        self.client = Client()
        self.client.force_login(self.user)
    
    def test_get_categories_table_part_resolves(self):
        response = self.client.get(reverse('blog:get_categories_table_part'))
        self.assertEqual(response.status_code, 200)
    
    def test_get_categories_table_part_template(self):
        response = self.client.get(reverse('blog:get_categories_table_part'))
        self.assertContains(response, '<!-- This is line for testing purposes. TEMPLATE: category_table.html -->')
        self.assertTemplateUsed(response, 'blog/components/category_table.html')
    
    def test_get_categories_table_part_context(self):
        response = self.client.get(reverse('blog:get_categories_table_part'))
        self.assertEqual(response.context['categories'][0], self.category)