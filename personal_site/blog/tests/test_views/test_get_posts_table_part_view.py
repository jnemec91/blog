from django.test import TestCase, Client
from django.urls import reverse, resolve
from blog.models import BlogUser, BlogPost, Category, HistoryLog
from blog.views import get_posts_table_part

class TestGetPostsTablePart(TestCase):
    def setUp(self):
        self.user = BlogUser.objects.create_user(email='test@test.test', password='test')
        self.category = Category.objects.create(name='test', description='test')
        self.post = BlogPost.objects.create(title='test', content='test', category=self.category, author=self.user)
        self.client = Client()
        self.client.force_login(self.user)
    
    def test_get_posts_table_part_resolves(self):
        response = self.client.get(reverse('blog:get_posts_table_part'))
        self.assertEqual(response.status_code, 200)
    
    def test_get_posts_table_part_template(self):
        response = self.client.get(reverse('blog:get_posts_table_part'))
        self.assertContains(response, '<!-- This is line for testing purposes. TEMPLATE: post_table.html -->')
        self.assertTemplateUsed(response, 'blog/components/post_table.html')
    
    def test_get_posts_table_part_context(self):
        response = self.client.get(reverse('blog:get_posts_table_part'))
        self.assertEqual(response.context['posts'][0], self.post)
    
    def test_get_posts_table_part_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('blog:get_posts_table_part'))
        self.assertRedirects(response, f'{reverse('blog:login')}?next={reverse("blog:get_posts_table_part")}')