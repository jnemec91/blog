from django.test import TestCase
from blog.models import HistoryLog

class HistoryLogModelTest(TestCase):
    def setUp(self):
        HistoryLog.objects.create(source="1:BlogUser object (1)", action="User created")
        HistoryLog.objects.create(source="1:Category object (1)", action="Category created")
        HistoryLog.objects.create(source="1:BlogPost object (1)", action="Blog created")


    def test_historylog_model_create(self):
        # get the history logs
        user_log = HistoryLog.objects.get(source="1:BlogUser object (1)")
        category_log = HistoryLog.objects.get(source="1:Category object (1)")
        blog_log = HistoryLog.objects.get(source="1:BlogPost object (1)")

        # assertions
        self.assertEqual(user_log.action, "User created")
        self.assertEqual(category_log.action, "Category created")
        self.assertEqual(blog_log.action, "Blog created")
    
    def test_historylog_model_update(self):
        # get the history logs
        user_log = HistoryLog.objects.get(source="1:BlogUser object (1)")
        category_log = HistoryLog.objects.get(source="1:Category object (1)")
        blog_log = HistoryLog.objects.get(source="1:BlogPost object (1)")

        # update the history logs
        user_log.action = "User updated"
        category_log.action = "Category updated"
        blog_log.action = "Blog updated"

        user_log.save()
        category_log.save()
        blog_log.save()
        
        # get the updated history logs
        user_log = HistoryLog.objects.get(id=user_log.pk)
        category_log = HistoryLog.objects.get(id=category_log.pk)
        blog_log = HistoryLog.objects.get(id=blog_log.pk)

        # assertions
        self.assertEqual(user_log.action, "User updated")
        self.assertEqual(category_log.action, "Category updated")
        self.assertEqual(blog_log.action, "Blog updated")
    
    def test_historylog_model_delete(self):
        # get the history logs
        user_log = HistoryLog.objects.get(source="1:BlogUser object (1)")
        category_log = HistoryLog.objects.get(source="1:Category object (1)")
        blog_log = HistoryLog.objects.get(source="1:BlogPost object (1)")
        
        # delete the history logs
        user_log.delete()
        category_log.delete()
        blog_log.delete()

        # get the updated history logs
        user_log = HistoryLog.objects.filter(source="1:BlogUser object (1)")
        category_log = HistoryLog.objects.filter(source="1:Category object (1)")
        blog_log = HistoryLog.objects.filter(source="1:BlogPost object (1)")
        
        # assertions
        self.assertEqual(len(user_log), 0)
        self.assertEqual(len(category_log), 0)
        self.assertEqual(len(blog_log), 0)
    
    def test_historylog_model_str(self):
        # get the history logs
        user_log = HistoryLog.objects.get(source="1:BlogUser object (1)")
        category_log = HistoryLog.objects.get(source="1:Category object (1)")
        blog_log = HistoryLog.objects.get(source="1:BlogPost object (1)")
        
        # assertions
        self.assertEqual(str(user_log), "1:BlogUser object (1) - User created")
        self.assertEqual(str(category_log), "1:Category object (1) - Category created")
        self.assertEqual(str(blog_log), "1:BlogPost object (1) - Blog created")
    
