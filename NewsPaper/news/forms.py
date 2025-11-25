from django import forms
from .models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

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

# форма регистрации для добавления пользователей в группу
class BasicSignupForm(SignupForm):
    
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='basic')
        basic_group.user_set.add(user)
        return user
