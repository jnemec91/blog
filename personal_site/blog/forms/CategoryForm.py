from django import forms
from blog.models import Category, HistoryLog

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

    def save(self):
        if self.instance.pk is None:
            super().save()
            HistoryLog.objects.create(source=f'{self.instance}', action='create')
        else:
            super().save()
            HistoryLog.objects.create(source=f'{self.instance}', action='update')

        return self.instance

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
