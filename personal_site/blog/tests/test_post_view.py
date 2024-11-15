from django.test import TestCase
from django.urls import reverse, resolve
from blog.models import BlogUser, BlogPost, Category
from blog.views import post


class TestPostView(TestCase):
    def setUp(self):
        self.user = BlogUser.objects.create_user(email='test@test.test', password='testpassword')
        self.category = Category.objects.create(name='test', description='test')
        self.post = BlogPost.objects.create(title='test', content='test', author=self.user, category=self.category)

    def test_post_url_resolves(self):
        url = reverse('blog:post', args=[self.post.hash_field])
        self.assertEqual(resolve(url).func, post)
    
    def test_post_view(self):
        response = self.client.get(reverse('blog:post', args=[self.post.hash_field]))
        self.assertEqual(response.status_code, 200)
    
    def test_post_view_template(self):
        response = self.client.get(reverse('blog:post', args=[self.post.hash_field]))
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertContains(response, '<!-- This is line for testing purposes. TEMPLATE: post_detail.html -->')
    
    def test_post_view_context(self):
        response = self.client.get(reverse('blog:post', args=[self.post.hash_field]))
        self.assertEqual(response.context['post'], self.post)