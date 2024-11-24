from django.test import TestCase, Client
from django.urls import reverse, resolve
from blog.views import update_navbar
from blog.models import Category, BlogPost, BlogUser


class Testupdate_navbarView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = BlogUser.objects.create_user(email='test@test.test', password='testpassword')
        self.category = Category.objects.create(name='Test Category', description='Test Description')
        self.post = BlogPost.objects.create(title='Test Title', content='Test Content', category=self.category, author=self.user, is_published=True)
    
    def test_update_navbar_url_resolves(self):
        url = reverse('blog:update_navbar')
        self.assertEqual(resolve(url).func, update_navbar)

    def test_update_navbar_view(self):
        response = self.client.get(reverse('blog:update_navbar'))
        self.assertEqual(response.status_code, 200)
    
    def test_update_navbar_view_template(self):
        response = self.client.get(reverse('blog:update_navbar'))
        self.assertTemplateUsed(response, 'blog/components/navbar.html')
        self.assertContains(response, '<!-- This is line for testing purposes. TEMPLATE: navbar.html -->')

    def test_update_navbar_view_context(self):
        response = self.client.get(reverse('blog:update_navbar'))
        self.assertEqual(response.context['categories'].count(), 1)
        self.assertEqual(response.context['latest'], self.post.hash_field)

        self.post.is_published = False
        self.post.save()
        response = self.client.get(reverse('blog:update_navbar'))
        self.assertEqual(response.context['categories'].count(), 0)
        self.assertIsNone(response.context['latest'])