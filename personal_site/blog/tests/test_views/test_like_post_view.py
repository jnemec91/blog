from django.test import TestCase
from django.urls import reverse, resolve
from blog.models import BlogPost, Category, Stats, BlogUser
from blog.views import like_post


class LikePostViewTest(TestCase):
    def setUp(self):
        self.user = BlogUser.objects.create_user(email='test@test.test', password='password')
        self.category = Category.objects.create(name='Test Category')
        self.post = BlogPost.objects.create(
            title='Test Post',
            content='Test Content',
            category=self.category,
            author=self.user,
        )
        
    def test_like_post_view_resolves(self):
        view = resolve(reverse('blog:like_post', args=[self.post.hash_field, 'like']))
        self.assertEqual(view.func, like_post)

        view = resolve(reverse('blog:like_post', args=[self.post.hash_field, 'dislike']))
        self.assertEqual(view.func, like_post)
    
    def test_like_post_view_redirects_to_post_detail(self):
        response = self.client.get(reverse('blog:like_post', args=[self.post.hash_field, 'like']))
        self.assertRedirects(response, reverse('blog:post_footer', args=[self.post.hash_field]))
    
    def test_like_post_view_increases_likes(self):
        self.client.get(reverse('blog:like_post', args=[self.post.hash_field, 'like']))
        self.post.refresh_from_db()
        self.assertEqual(self.post.stats.likes, 1)
    
    def test_like_post_view_increases_dislikes(self):
        self.client.get(reverse('blog:like_post', args=[self.post.hash_field, 'dislike']))
        self.post.refresh_from_db()
        self.assertEqual(self.post.stats.dislikes, 1)
    
    def test_like_post_view_does_not_increase_likes_if_already_voted(self):
        self.client.get(reverse('blog:like_post', args=[self.post.hash_field, 'like']))
        self.client.get(reverse('blog:like_post', args=[self.post.hash_field, 'like']))
        self.post.refresh_from_db()
        self.assertEqual(self.post.stats.likes, 1)
    
    def test_like_post_view_does_not_increase_dislikes_if_already_voted(self):
        self.client.get(reverse('blog:like_post', args=[self.post.hash_field, 'dislike']))
        self.client.get(reverse('blog:like_post', args=[self.post.hash_field, 'dislike']))
        self.post.refresh_from_db()
        self.assertEqual(self.post.stats.dislikes, 1)
    
    def test_like_post_view_does_not_increase_likes_if_disliked(self):
        self.client.get(reverse('blog:like_post', args=[self.post.hash_field, 'dislike']))
        self.client.get(reverse('blog:like_post', args=[self.post.hash_field, 'like']))
        self.post.refresh_from_db()
        self.assertEqual(self.post.stats.likes, 0)
    
    def test_like_post_view_does_not_increase_dislikes_if_liked(self):
        self.client.get(reverse('blog:like_post', args=[self.post.hash_field, 'like']))
        self.client.get(reverse('blog:like_post', args=[self.post.hash_field, 'dislike']))
        self.post.refresh_from_db()
        self.assertEqual(self.post.stats.dislikes, 0)