from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse



# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    
    # Метод обновление рейтинга
    def update_rating(self):
        posts_rating = self.posts.aggregate(total=models.Sum('rating'))['total'] or 0
        posts_rating *= 3
        
        comments_rating = self.user.comment_set.aggregate(total=models.Sum('rating'))['total'] or 0
        
        comments_on_posts_rating = Comment.objects.filter(post__author=self).aggregate(total=models.Sum('rating'))['total'] or 0
        
        self.rating = posts_rating + comments_rating + comments_on_posts_rating
        self.save()

        def __str__(self):
            return f'Author: {self.user.username} (rating: {self.rating})'
        
class Category(models.Model):
    name = models.CharField(max_length = 255, unique=True)
    subscribers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        through='news.Subscription',
        related_name='subscribed_categories',
        blank=True
    )
    
    def __str__(self):
        return self.name
    
class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'
    POST_TYPES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость')
    ]
    
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=ARTICLE)
    create_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('Category', through='PostCategory')
    title = models.CharField(max_length= 255)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    
    # Метод лайк
    def like(self):
        self.rating += 1
        self.save()
        
    # Метод дизлайк
    def dislike(self):
        self.rating -= 1
        self.save()
    
    # Метод ревью 
    def preview(self):
        return self.text[:124] + '...'
    
    def __str__(self):
        return f'{self.title} ({self.get_post_type_display()})'
    
    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])
        

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post.title} -> {self.category.name}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    
    def like(self):
        self.rating += 1
        self.save()
        
    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'
    
    
class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'category']
