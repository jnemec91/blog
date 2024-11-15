from django.test import TestCase, Client
from django.urls import reverse, resolve
from blog.models import Category, BlogPost, BlogUser
from blog.views import category


class TestCategoryView(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Test Category', description='Test Description')
        self.user = BlogUser.objects.create_user(email='test@test.test', password='testpassword')
        self.post = BlogPost.objects.create(title='Test Post', content='Test Content', category=self.category, author=self.user)

    def test_category_view(self):
        response = self.client.get(reverse('blog:category', args=[self.category.hash_field]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/posts.html')
        self.assertEqual(response.context['category'], self.category)
        self.assertTrue(self.post in response.context['posts'])

    def test_category_url_resolves_category_view(self):
        view = resolve(reverse('blog:category', args=[self.category.hash_field]))
        self.assertEqual(view.func, category)

    def test_category_view_template(self):
        response = self.client.get(reverse('blog:category', args=[self.category.hash_field]))
        self.assertTemplateUsed(response, 'blog/posts.html')
        self.assertContains(response, '<!-- This is line for testing purposes. TEMPLATE: posts.html -->')
    
    def test_category_view_context(self):
        response = self.client.get(reverse('blog:category', args=[self.category.hash_field]))
        self.assertEqual(response.context['category'], self.category)
        self.assertTrue(self.post in response.context['posts'])
        self.assertEqual(response.context['posts'].first().title, 'Test Post')
        self.assertEqual(response.context['posts'].first().content, 'Test Content')
        self.assertEqual(response.context['posts'].first().category, self.category)
        self.assertEqual(response.context['posts'].first().author, self.user)