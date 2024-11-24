from django.test import TestCase, Client
from django.urls import reverse, resolve
from blog.models import BlogPost, BlogUser, Category
from blog.views import post_delete

class TestPostDeleteView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = BlogUser.objects.create_user(email='testuser@test.test', password='password')
        self.client.force_login(user=self.user)
        self.category = Category.objects.create(name='Test Category', description='Test Description')
        self.post = BlogPost.objects.create(title='Test Post', content='Test Content', category=self.category, is_published=True, author=self.user)
    
    def test_post_delete_view_url_resolves(self):
        url = reverse('blog:post_delete', args=[self.post.hash_field])
        self.assertEqual(resolve(url).func, post_delete)
    
    def test_post_delete_view(self):
        response = self.client.delete(reverse('blog:post_delete', args=[self.post.hash_field]))
        self.assertEqual(response.status_code, 302)
    
    def test_post_delete_view_post_deleted(self):
        self.client.delete(reverse('blog:post_delete', args=[self.post.hash_field]))
        self.assertEqual(len(BlogPost.objects.filter(title='Test Post')), 0)

    def test_post_delete_unauthenticated(self):
        self.client.logout()
        response = self.client.delete(reverse('blog:post_delete', args=[self.post.hash_field]))
        self.assertRedirects(response, f'{reverse('blog:login')}?next={reverse("blog:post_delete", args=[self.post.hash_field])}')
        self.assertEqual(len(BlogPost.objects.filter(title='Test Post')), 1)