from django.test import TestCase
from django.urls import reverse, resolve
from blog.models import Category, HistoryLog
from blog.views import category_edit
from blog.forms import CategoryForm

class TestCategoryEditView(TestCase):
    def setUp(self):
        # create a category
        self.category = Category.objects.create(name="test category", description="test description")

    def test_category_edit_view_url_resolves(self):
        url = reverse('blog:category_edit')
        self.assertEqual(resolve(url).func, category_edit)

    def test_category_edit_view_get_no_instance(self):
        response = self.client.get(reverse('blog:category_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/category_edit.html')
        self.assertEqual(response.context['form'].instance.pk, None)
    
    def test_category_edit_view_get_instance(self):
        response = self.client.get(reverse('blog:category_edit', args=[self.category.hash_field]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/category_edit.html')
        self.assertEqual(response.context['form'].instance, self.category)
    
    def test_category_edit_view_post(self):
        response = self.client.post(reverse('blog:category_edit', args=[self.category.hash_field]), {
            'name': 'updated category',
            'description': 'updated description',
        })
        self.assertRedirects(response, reverse('blog:categories_admin'))
        self.assertEqual(Category.objects.get(name="updated category").description, 'updated description')
        self.assertEqual(HistoryLog.objects.last().action, "update")
    
    def test_category_edit_view_post_invalid(self):
        response = self.client.post(reverse('blog:category_edit', args=[self.category.hash_field]), {
            'name': 'updated category',
            'description': '',
        })
        self.assertEqual(response.status_code, 302)
