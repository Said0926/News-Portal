from django import forms
from .models import Post

class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'categories']
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.post_type = 'NW'  # Новость
        if commit:
            instance.save()
            self.save_m2m()
        return instance

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'categories']
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.post_type = 'AR'  # Статья
        if commit:
            instance.save()
            self.save_m2m()
        return instance