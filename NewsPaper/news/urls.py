from django.urls import path
from .views import (
    NewsDetail, NewsList, 
    create_article, create_news, delete_article, delete_news, edit_article, edit_news,
    become_author, 
    subscribe_to_category, unsubscribe_from_category, my_subscriptions,
    
    )

urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    
    # Новости
    path('news/create/', create_news, name='news_create'),
    path('news/<int:pk>/edit/', edit_news, name='news_edit'),
    path('news/<int:pk>/delete/', delete_news, name='news_delete'),
    
    # Статьи
    path('articles/create/', create_article, name='article_create'),
    path('articles/<int:pk>/edit/', edit_article, name='article_edit'),
    path('articles/<int:pk>/delete/', delete_article, name='article_delete'),

    # стать автором 
    path('become-author/', become_author, name='become_author'),
    
    # Подписки
    path('category/<int:category_id>/subscribe/', subscribe_to_category, name='subscribe_to_category'),
    path('category/<int:category_id>/unsubscribe/', unsubscribe_from_category, name='unsubscribe_from_category'),
    path('subscriptions/', my_subscriptions, name='my_subscriptions'),
]
