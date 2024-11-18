from django.test import TestCase, Client
from django.urls import reverse, resolve
from blog.models import BlogPost, Category, BlogUser
from blog.views import latest

class TestLatestView(TestCase):
        
        def setUp(self):
            self.client = Client()
            self.latest_url = reverse('blog:latest')
            self.latest_post = BlogPost.objects.create(
                title='Test Post',
                content='Test Content',
                category=Category.objects.create(name='Test Category'),
                author=BlogUser.objects.create_user(email='test@test.test', password='test')
            )
        
        def test_latest_url_resolves(self):
            response = self.client.get(self.latest_url)
            self.assertEqual(resolve(self.latest_url).func, latest)
        
        def test_latest_view(self):
            response = self.client.get(self.latest_url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Test Post')
            self.assertContains(response, 'Test Content')
            self.assertContains(response, 'Test Category')
        
        def test_latest_view_template(self):
            response = self.client.get(self.latest_url)
            self.assertTemplateUsed(response, 'blog/post_detail.html')
            self.assertContains(response, '<!-- This is line for testing purposes. TEMPLATE: post_detail.html -->')
