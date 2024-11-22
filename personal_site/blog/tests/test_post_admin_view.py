from django.test import TestCase, Client
from django.urls import reverse, resolve
from blog.models import BlogUser, BlogPost, Category, HistoryLog

class TestPostAdmin(TestCase):
    def setUp(self):
        self.user = BlogUser.objects.create_user(email='test@test.test', password='test')
        self.category = Category.objects.create(name='test', description='test')
        self.post = BlogPost.objects.create(title='test', content='test', category=self.category, author=self.user)
        self.client = Client()
        self.client.login()
    
    def test_post_admin_resolves(self):
        response = self.client.get(reverse('blog:posts_admin'))
        self.assertEqual(response.status_code, 200)

    def test_post_admin_template(self):
        response = self.client.get(reverse('blog:posts_admin'))
        self.assertContains(response, '<!-- This is line for testing purposes. TEMPLATE: posts_admin.html -->')
        self.assertTemplateUsed(response, 'blog/posts_admin.html')
