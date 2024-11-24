from django.test import TestCase, Client
from django.urls import reverse, resolve
from blog.models import BlogPost, Category, Stats, BlogUser
from blog.views import stats


# @login_required
# def stats(request):
#     # get number of users, posts, categories, and logs
#     users = BlogUser.objects.all().count()
#     posts = BlogPost.objects.all().count()
#     categories = Category.objects.all().count()

#     # get stats for top 10 posts
#     top_posts = BlogPost.objects.all().order_by('-stats__views')[:10]
#     most_liked = BlogPost.objects.all().order_by('-stats__likes')[:10]
#     most_disliked = BlogPost.objects.all().order_by('stats__dislikes')[:10]
    

#     return render(request, 'blog/stats.html',
#         {'users': users, 'posts': posts, 'categories': categories,
#             'top_posts': top_posts, 'most_liked': most_liked, 'most_disliked': most_disliked}
#                   )

class TestStatsView(TestCase):
    
        def setUp(self):
            self.client = Client()
            self.category = Category.objects.create(name='Test Category', description='Test Description')
            self.user = BlogUser.objects.create_user(email='test@test.test', password='password')
            self.post = BlogPost.objects.create(title='Test Title', content='Test Content', category=self.category, author=self.user)
            self.client.force_login(self.user)

        def test_stats_resolves(self):
            view = resolve(reverse('blog:stats'))
            self.assertEqual(view.func, stats)

        def test_stats_view(self):
            response = self.client.get(reverse('blog:stats'))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context['users'], 1)
            self.assertEqual(response.context['posts'], 1)
            self.assertEqual(response.context['categories'], 1)
            self.assertEqual(response.context['top_posts'].count(), 1)
            self.assertEqual(response.context['most_liked'].count(), 1)
            self.assertEqual(response.context['most_disliked'].count(), 1)
            self.assertTemplateUsed(response, 'blog/stats.html')
            self.assertContains(response, '<!-- This is line for testing purposes. TEMPLATE: stats.html -->')
        
        def test_stats_view_no_data(self):
            BlogPost.objects.all().delete()
            Category.objects.all().delete()
            # ofc user cant be deleted, because it is used to login
            response = self.client.get(reverse('blog:stats'))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context['users'], 1)
            self.assertEqual(response.context['posts'], 0)
            self.assertEqual(response.context['categories'], 0)
            self.assertEqual(response.context['top_posts'].count(), 0)
            self.assertEqual(response.context['most_liked'].count(), 0)
            self.assertEqual(response.context['most_disliked'].count(), 0)
            self.assertTemplateUsed(response, 'blog/stats.html')
            self.assertContains(response, '<!-- This is line for testing purposes. TEMPLATE: stats.html -->')
        
        def test_stats_view_unauthenticated(self):
            self.client.logout()
            response = self.client.get(reverse('blog:stats'))
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, f'{reverse('blog:login')}?next={reverse("blog:stats")}')