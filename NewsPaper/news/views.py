from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from .models import Post, Author
from .forms import NewsForm, ArticleForm
from .filters import PostFilter

class NewsList(ListView):
    model = Post
    ordering = '-create_at'
    template_name = 'news_list.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class NewsDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'post'

# СОЗДАНИЕ
# @login_required
def create_news(request):
    if not hasattr(request.user, 'author'):
        Author.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user.author
            news.post_type = 'NW'
            news.save()
            form.save_m2m()
            return redirect('news_list')
    else:
        form = NewsForm()
    
    return render(request, 'news_create.html', {'form': form})

# @login_required
def create_article(request):
    if not hasattr(request.user, 'author'):
        Author.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user.author
            article.post_type = 'AR'
            article.save()
            form.save_m2m()
            return redirect('news_list')
    else:
        form = ArticleForm()
    
    return render(request, 'article_create.html', {'form': form})


# РЕДАКТИРОВАНИЕ
# @login_required
def edit_news(request, pk):
    news = get_object_or_404(Post, pk=pk, post_type='NW')
    
    # Проверяем, что пользователь - автор новости
    if news.author != request.user.author:
        return redirect('news_list')
    
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            return redirect('news_detail', pk=news.pk)
    else:
        form = NewsForm(instance=news)
    
    return render(request, 'news_edit.html', {'form': form, 'news': news})

# @login_required
def edit_article(request, pk):
    article = get_object_or_404(Post, pk=pk, post_type='AR')
    
    # Проверяем, что пользователь - автор статьи
    if article.author != request.user.author:
        return redirect('news_list')
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('news_detail', pk=article.pk)
    else:
        form = ArticleForm(instance=article)
    
    return render(request, 'article_edit.html', {'form': form, 'article': article})

# УДАЛЕНИЕ
# @login_required
def delete_news(request, pk):
    news = get_object_or_404(Post, pk=pk, post_type='NW')
    
    # Проверяем, что пользователь - автор новости
    if news.author != request.user.author:
        return redirect('news_list')
    
    if request.method == 'POST':
        news.delete()
        return redirect('news_list')
    
    return render(request, 'news_delete.html', {'news': news})

# @login_required
def delete_article(request, pk):
    article = get_object_or_404(Post, pk=pk, post_type='AR')
    
    # Проверяем, что пользователь - автор статьи
    if article.author != request.user.author:
        return redirect('news_list')
    
    if request.method == 'POST':
        article.delete()
        return redirect('news_list')
    
    return render(request, 'article_delete.html', {'article': article})
