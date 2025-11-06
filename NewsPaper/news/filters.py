from django_filters import FilterSet
from .models import Post

class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            # поиск по названию
            'title': ['icontains'],
            # поиск по тексту
            'text': ['icontains'],
            # фильтр по типу поста (статья или новость)
            'post_type': ['exact'],
            # фильтр по автору
            'author': ['exact'],
            # рейтинг должен быть больше или равен
            'rating': ['gt'],
            # дата создания должна быть после указанной
            'create_at': ['gt'],
        }