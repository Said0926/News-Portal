from django.views.generic import ListView, DetailView
from .models import Post
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