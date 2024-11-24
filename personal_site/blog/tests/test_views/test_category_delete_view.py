from django.test import TestCase, Client
from django.urls import reverse, resolve
from blog.models import Category, BlogUser
from blog.views import category_delete


class TestPostDeleteView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = BlogUser.objects.create_user(email="test@test.test", password="test")
        self.category = Category.objects.create(name='Test Category', description='Test Description')
        self.client.force_login(self.user)

    def test_category_delete_view_url_resolves(self):
        url = reverse('blog:category_delete', args=[self.category.hash_field])
        self.assertEqual(resolve(url).func, category_delete)
    
    def test_category_delete_view(self):
        response = self.client.delete(reverse('blog:category_delete', args=[self.category.hash_field]))
        self.assertEqual(response.status_code, 302)
    
    def test_category_delete_view_post_deleted(self):
        response = self.client.delete(reverse('blog:category_delete', args=[self.category.hash_field]))
        self.assertEqual(len(Category.objects.filter(hash_field=self.category.hash_field)), 0)
    
    def test_category_delete_unauthenticated(self):
        self.client.logout()
        response = self.client.delete(reverse('blog:category_delete', args=[self.category.hash_field]))
        self.assertRedirects(response, f'{reverse('blog:login')}?next={reverse("blog:category_delete", args=[self.category.hash_field])}')
        self.assertEqual(len(Category.objects.filter(name='Test Category')), 1)
    