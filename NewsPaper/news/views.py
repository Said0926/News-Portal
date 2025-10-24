# from django.views.generic import ListView
# from django.shortcuts import render
# from .models import *

# # Create your views here.
# class NewsList(ListView):
#     model = Post
#     ordering = 'title'
#     template_name = 'news.html'
#     context_object_name = 'products'

from django.shortcuts import render, get_object_or_404
from .models import Post

def news_list(request):
    # Получаем все посты (и статьи, и новости)
    posts = Post.objects.all().order_by('-create_at')
    return render(request, 'news_list.html', {'posts': posts})

def news_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'news_detail.html', {'post': post})