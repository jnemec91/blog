from django.test import TestCase
from blog.models import Category, HistoryLog

class TestCategoryModel(TestCase):
    def setUp(self):
        # clear the database
        Category.objects.all().delete()

        # create a category
        Category.objects.create(name="test category", description="test description")

    def test_category_create(self):
        # get the category
        category = Category.objects.get(name="test category")

        # assertions
        self.assertEqual(category.name, "test category")
        self.assertEqual(category.description, "test description")

        # assert history log message was created
        self.assertEqual(HistoryLog.objects.last().action, "Category created")
        self.assertEqual(HistoryLog.objects.last().source, f"None:{category}")
    
    def test_category_update(self):
        # get the category
        category = Category.objects.get(name="test category")

        # update the category
        category.name = "updated category"
        category.description = "updated description"
        category.save()

        # get the updated category
        category = Category.objects.get(id=category.pk)

        # assertions
        self.assertEqual(category.name, "updated category")
        self.assertEqual(category.description, "updated description")
        
        # assert history log message was created
        self.assertEqual(HistoryLog.objects.last().action, "Category updated")
        self.assertEqual(HistoryLog.objects.last().source, f"{category.pk}:{category}")
    
    def test_category_delete(self):
        # get the category
        category = Category.objects.get(name="test category")
        id = category.pk
        # delete the category
        category.delete()

        # assert history log message was created
        self.assertEqual(HistoryLog.objects.last().action, "Category deleted")
        self.assertEqual(HistoryLog.objects.last().source, f"{id}:{category}")

    def test_category_str(self):
        # get the category
        category = Category.objects.get(name="test category")

        # assertions
        self.assertEqual(str(category), "test category")