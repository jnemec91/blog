from django import forms
from blog.models import BlogPost, Category, BlogUser, HistoryLog


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'image', 'content', 'category', 'is_published']

    def save(self):
        if self.instance.pk is None:
            self.instance.author = self.user
            super().save()
            HistoryLog.objects.create(source=f'{self.instance}', action='create')
            
        else:
            super().save(self.instance)
            HistoryLog.objects.create(source=f'{self.instance}', action='update')
        
        return self.instance


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Pass user to form
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
