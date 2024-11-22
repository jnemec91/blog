from django.test import TestCase, Client
from django.urls import reverse, resolve
from blog.models import Category
from blog.views import category_delete

class TestPostDeleteView(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Test Category', description='Test Description')

    def test_category_delete_view_url_resolves(self):
        url = reverse('blog:category_delete', args=[self.category.hash_field])
        self.assertEquals(resolve(url).func, category_delete)
    
    def test_category_delete_view(self):
        response = self.client.delete(reverse('blog:category_delete', args=[self.category.hash_field]))
        self.assertEquals(response.status_code, 302)
    
    def test_category_delete_view_post_deleted(self):
        self.client.delete(reverse('blog:category_delete', args=[self.category.hash_field]))
        self.assertEquals(len(Category.objects.filter(name='Test Category')), 0)
    