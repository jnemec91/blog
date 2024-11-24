from django import forms
from blog.models import BlogPost, Category, BlogUser


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'image', 'content', 'category', 'is_published']

    def save(self):
        if self.instance.pk is None:
            self.instance.author = self.user
            super().save()
            
        else:
            super().save(self.instance)
        
        return self.instance


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Pass user to form
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
