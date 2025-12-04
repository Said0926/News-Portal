from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Category, Post

def send_mails():
    print('Hello from backgraund task!')
    
def send_weekly_digest():
    """
    Основная функция еженедельной рассылки
    """
    print("=== Начало еженедельной рассылки ===")
    
    # 1. Получаем дату неделю назад
    week_ago = timezone.now() - timedelta(days=7)
    
    # 2. Находим все посты за неделю
    recent_posts = Post.objects.filter(
        create_at__gte=week_ago
    ).prefetch_related('categories')
    
    if not recent_posts.exists():
        print("Нет новых постов за неделю")
        return
    
    print(f"Найдено {recent_posts.count()} новых постов")
    
    # 3. Для каждой категории
    for category in Category.objects.all():
        # Находим посты этой категории
        category_posts = recent_posts.filter(categories=category)
        
        if not category_posts.exists():
            continue
        
        # Получаем подписчиков категории
        subscribers = category.subscribers.all()
        
        if not subscribers.exists():
            continue
        
        print(f"Категория '{category.name}': {category_posts.count()} постов, {subscribers.count()} подписчиков")
        
        # 4. Отправляем каждому подписчику
        for subscriber in subscribers:
            if not subscriber.email:
                continue
            
            try:
                subject = f'Новые статьи в категории "{category.name}" за неделю'
                
                # HTML версия
                html_message = render_to_string(
                    'account/email/weekly_digest.html',  # HTML шаблон
                    {
                        'user': subscriber,
                        'category': category,
                        'posts': category_posts,
                    }
                )
                
                # Текстовая версия  
                text_message = render_to_string(
                    'account/email/weekly_digest.txt',  # TXT шаблон
                    {
                        'user': subscriber,
                        'category': category,
                        'posts': category_posts,
                    }
                )
                
                send_mail(
                    subject=subject,
                    message=text_message,  # Текстовая версия
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[subscriber.email],
                    html_message=html_message,  # HTML версия
                    fail_silently=True,
                )
                
            except Exception as e:
                print(f"Ошибка: {e}")
    
    print("=== Рассылка завершена ===")