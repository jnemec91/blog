from django import forms
from blog.models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

    def save(self):
        if self.instance.pk is None:
            super().save()
        else:
            super().save()

        return self.instance

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
