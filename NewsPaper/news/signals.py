from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Post

@receiver(post_save, sender=Post)
def send_new_post_notifications(sender, instance, created, **kwargs):
    """
    Отправляет email уведомления всем подписчикам категорий новой статьи/новости
    """
    # Отправляем уведомления только при создании новой записи
    if not created:
        return
    
    # Получаем все категории поста
    categories = instance.categories.all()
    
    if not categories.exists():
        return
    
    # Проходим по всем категориям поста
    for category in categories:
        # Получаем всех подписчиков категории
        subscribers = category.subscribers.all()
        
        if not subscribers.exists():
            continue
        
        # Отправляем уведомления каждому подписчику
        for subscriber in subscribers:
            try:
                # Проверяем, есть ли у пользователя email
                if not subscriber.email:
                    continue
                
                # Формируем тему письма (заголовок статьи)
                subject = f'{instance.title}'
                
                # Создаем HTML сообщение
                html_message = render_to_string('email/new_post_notification.html', {
                    'post': instance,
                    'user': subscriber,
                    'category': category,
                })
                
                # Создаем текстовую версию письма
                text_message = f"""
Здравствуй, {subscriber.username}. Новая статья в твоём любимом разделе!

Заголовок: {instance.title}

Текст: {instance.text[:50]}...

Категория: {category.name}
Автор: {instance.author.user.username}
Дата: {instance.create_at.strftime('%d.%m.%Y %H:%M')}

Читать полностью: http://127.0.0.1:8000/news/{instance.id}/

---
Вы получили это письмо, потому что подписаны на категорию "{category.name}"
Управление подписками: http://127.0.0.1:8000/news/subscriptions/
                """
                
                # Отправляем email
                send_mail(
                    subject=subject,
                    message=text_message.strip(),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[subscriber.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                
            except Exception:
                # Просто игнорируем ошибки отправки
                pass