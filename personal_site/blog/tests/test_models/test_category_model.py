from django.test import TestCase
from blog.models import Category, HistoryLog
from blog.utils.hashmaker import make_hash_from_model

class TestCategoryModel(TestCase):
    def setUp(self):
        Category.objects.all().delete()
        Category.objects.create(name="test category", description="test description")

    def test_category_create(self):
        category = Category.objects.get(name="test category")
        self.assertEqual(category.name, "test category")
        self.assertEqual(category.description, "test description")
        self.assertEqual(HistoryLog.objects.last().action, "Category created")
        self.assertEqual(HistoryLog.objects.last().source, f"NEW:{category}")
    
    def test_category_update(self):
        category = Category.objects.get(name="test category")
        category.name = "updated category"
        category.description = "updated description"
        category.save()
        category = Category.objects.get(id=category.pk)
        self.assertEqual(category.name, "updated category")
        self.assertEqual(category.description, "updated description")
        self.assertEqual(HistoryLog.objects.last().action, "Category updated")
        self.assertEqual(HistoryLog.objects.last().source, f"{category.pk}:{category}")
    
    def test_category_delete(self):
        category = Category.objects.get(name="test category")
        id = category.pk
        category.delete()
        self.assertEqual(HistoryLog.objects.last().action, "Category deleted")
        self.assertEqual(HistoryLog.objects.last().source, f"{id}:{category}")

    def test_category_str(self):
        category = Category.objects.get(name="test category")
        self.assertEqual(str(category), "Category: test category")
    
    def test_category_hash_field(self):
        category = Category.objects.get(name="test category")
        self.assertEqual(len(category.hash_field), 32)
        self.assertEqual(category.hash_field, make_hash_from_model(category))
