from django.test import TestCase
from blog.forms.BlogPostForm import BlogPostForm
from blog.models import BlogPost, Category, BlogUser, HistoryLog


class TestBlogPostForm(TestCase):
    def setUp(self):
        self.user = BlogUser.objects.create(email='test@test.test', password='password')
        self.category = Category.objects.create(name='test', description='test')
        self.blog_post = BlogPost.objects.create(title='test', content='test', category=self.category, author=self.user)

    def test_blog_post_form_valid(self):
        form = BlogPostForm(data={'title': 'test', 'content': 'test', 'category': self.category.pk, 'is_published': True}, user=self.user)
        self.assertTrue(form.is_valid())

    def test_blog_post_form_invalid(self):
        form = BlogPostForm(data={'title': 'test', 'content': 'test', 'category': 'invalid', 'is_published': True})
        self.assertFalse(form.is_valid())
    
    def test_blog_post_form_save(self):
        form = BlogPostForm(data={'title': 'test_save', 'content': 'test', 'category': self.category.pk, 'is_published': True}, user=self.user)
        form.is_valid()
        post = form.save()
        self.assertTrue(BlogPost.objects.filter(title='test_save').exists())
        self.assertTrue(HistoryLog.objects.filter(source=post, action='create').exists())
    
    def test_blog_post_form_update(self):
        form = BlogPostForm(instance=self.blog_post, data={'title': 'test_update', 'content': 'test', 'category': self.category.pk, 'is_published': True}, user=self.user)
        form.is_valid()
        form.save()
        self.assertTrue(BlogPost.objects.filter(title='test_update').exists())
        self.assertTrue(HistoryLog.objects.filter(source=self.blog_post, action='update').exists())

