from django.test import TestCase, Client
from django.urls import reverse, resolve
from blog.models import BlogUser, BlogPost, Category, HistoryLog
from blog.views import posts


class TestpostsView(TestCase):
    def setUp(self):
        self.user = BlogUser.objects.create_user(
            email='test@test.test',
            password='testpassword',
        )
        self.category = Category.objects.create(
            name='testcategory',
            hash_field='testcategory',
        )
        self.post = BlogPost.objects.create(
            title='testpost',
            content='testcontent',
            category=self.category,
            author=self.user,
        )
        self.client = Client()
    
    def test_posts_url_resolves(self):
        url = reverse('blog:posts')
        self.assertEqual(resolve(url).func, posts)

    def test_posts_view(self):
        response = self.client.get(reverse('blog:posts'))
        self.assertEqual(response.status_code, 200)
    
    def test_posts_view_template(self):
        response = self.client.get(reverse('blog:posts'))
        self.assertTemplateUsed(response, 'blog/posts.html')
        self.assertContains(response, '<!-- This is line for testing purposes. TEMPLATE: posts.html -->')

    def test_posts_view_context(self):
        response = self.client.get(reverse('blog:posts'))
        self.assertEqual(response.context['posts'][0].title, 'testpost')
        self.assertEqual(response.context['posts'][0].content, 'testcontent')
        self.assertEqual(response.context['posts'][0].category.name, 'testcategory')
        self.assertEqual(response.context['posts'][0].author.email, 'test@test.test')