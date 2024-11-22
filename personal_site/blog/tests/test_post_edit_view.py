from django.test import TestCase, Client
from django.urls import reverse, resolve
from blog.models import BlogPost, Category, BlogUser
from blog.views import post_edit
from django.db.models import QuerySet

class TestPostEdit(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='test', description='test')
        self.user = BlogUser.objects.create_user(email='test@test.test', password='test')
        self.new_category = Category.objects.create(name='new', description='new')
        self.post = BlogPost.objects.create(title='test', content='test', category=self.category, author=self.user, is_published=True)
        self.client = Client()
        self.client.force_login(user=self.user)

    def test_post_edit_resolves(self):
        response = self.client.get(reverse('blog:post_edit'))
        self.assertEqual(response.status_code, 200)

    def test_post_edit_template(self):
        response = self.client.get(reverse('blog:post_edit'))
        self.assertContains(response, '<!-- This is line for testing purposes. TEMPLATE: post_edit.html -->')
    
    def test_post_edit_context_get_no_instance(self):
        response = self.client.get(reverse('blog:post_edit'))
        self.assertEqual(response.context['form'].instance.pk, None)
    
    def test_post_edit_context_get_instance(self):
        response = self.client.get(reverse('blog:post_edit', args=[self.post.hash_field]))
        self.assertEqual(response.context['form'].instance, self.post)
        self.assertEqual(response.context['form'].instance.author, self.user)
        self.assertEqual(response.context['form'].instance.category, self.category)
    
    def test_post_edit_new(self):
        response = self.client.post(reverse('blog:post_edit'), {
            'title': 'new',
            'content': 'new',
            'category': self.new_category.pk,
            'author': self.user.pk,
            'is_published': True,
        })
        self.assertEqual(BlogPost.objects.get(title='new').category, self.new_category)
        self.assertEqual(BlogPost.objects.get(title='new').author, self.user)

    def test_post_edit_post_instance(self):
        response = self.client.post(reverse('blog:post_edit', args=[self.post.hash_field]), {
            'title': 'new',
            'content': 'new',
            'category': self.new_category.pk,
            'author': self.user.pk,
            'is_published': True,
        })
        self.assertEqual(len(BlogPost.objects.filter(title='test')), 0)
        self.assertEqual(BlogPost.objects.get(title='new').category, self.new_category)
        self.assertEqual(BlogPost.objects.get(title='new').author, self.user)
