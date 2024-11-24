from django.test import TestCase
from blog.forms.CategoryForm import CategoryForm
from blog.models import Category, BlogUser, HistoryLog


class TestCategoryForm(TestCase):
    def setUp(self):
        self.user = BlogUser.objects.create(email='test@test.test', password='password')
        self.category = Category.objects.create(name='test', description='test')
    
    def test_category_form_valid(self):
        form = CategoryForm(instance=self.category, data={'name': 'test', 'description': 'test'},)
        self.assertTrue(form.is_valid())

    def test_category_form_invalid(self):
        form = CategoryForm(instance=self.category, data={'description': 'test'})
        self.assertFalse(form.is_valid())
    
    def test_category_form_save(self):
        form = CategoryForm(data={'name': 'test_save', 'description': 'test'},)
        form.is_valid()
        category = form.save()
        self.assertTrue(Category.objects.filter(name='test_save').exists())
        self.assertTrue(HistoryLog.objects.filter(source=f'NEW:{category}', action='Category created').exists())
    
    def test_category_form_update(self):
        form = CategoryForm(instance=self.category, data={'name': 'test_update', 'description': 'test'},)
        form.is_valid()
        form.save()
        self.assertTrue(Category.objects.filter(name='test_update').exists())
        self.assertTrue(HistoryLog.objects.filter(source=f'{self.category.pk}:{self.category}', action='Category updated').exists())
    