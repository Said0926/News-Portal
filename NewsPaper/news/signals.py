from django.db.models.signals import post_save, post_delete
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail, mail_managers
from django.template.loader import render_to_string
from django.conf import settings
from .models import Post

# @receiver(post_save, sender=Post)
# def send_new_post_notifications(sender, instance, created, **kwargs):
#     """
#     Отправляет email уведомления всем подписчикам категорий новой статьи/новости
#     """
    
#     # Отправляем уведомления только при создании новой записи
#     if not created:
#         return
    
#     # Получаем все категории поста
#     categories = instance.categories.all()
    
#     if not categories.exists():
#         return
    
#     # Проходим по всем категориям поста
#     for category in categories:
#         # Получаем всех подписчиков категории
#         subscribers = category.subscribers.all()
        
#         if not subscribers.exists():
#             continue
        
#         # Отправляем уведомления каждому подписчику
#         for subscriber in subscribers:
#             try:
#                 # Проверяем, есть ли у пользователя email
#                 if not subscriber.email:
#                     continue
                
#                 # Формируем тему письма (заголовок статьи)
#                 subject = f'{instance.title}'
                
#                 # Создаем HTML сообщение
#                 html_message = render_to_string('account/email/new_post_notification.html', {
#                     'post': instance,
#                     'user': subscriber,
#                     'category': category,
#                 })
                
#                 # Создаем текстовую версию письма
#                 text_message = f"""
# Здравствуй, {subscriber.username}. Новая статья в твоём любимом разделе!

# Заголовок: {instance.title}

# Текст: {instance.text[:50]}...

# Категория: {category.name}
# Автор: {instance.author.user.username}
# Дата: {instance.create_at.strftime('%d.%m.%Y %H:%M')}

# Читать полностью: http://127.0.0.1:8000/news/{instance.id}/

# ---
# Вы получили это письмо, потому что подписаны на категорию "{category.name}"
# Управление подписками: http://127.0.0.1:8000/news/subscriptions/
#                 """
                
#                 # Отправляем email
#                 send_mail(
#                     subject=subject,
#                     message=text_message.strip(),
#                     from_email=settings.DEFAULT_FROM_EMAIL,
#                     recipient_list=[subscriber.email],
#                     html_message=html_message,
#                     fail_silently=False,
#                 )
                
#             except Exception:
#                 # Просто игнорируем ошибки отправки
#                 pass

@receiver(m2m_changed, sender=Post.categories.through)
def send_new_post_notifications(sender, instance, action, **kwargs):
    """
    Отправляет email уведомления подписчикам при добавлении категорий к посту
    """
    # Нас интересует только добавление категорий
    if action != "post_add":
        return
    
    # Получаем добавленные категории
    pk_set = kwargs.get('pk_set', set())
    if not pk_set:
        return
    
    from .models import Category
    
    # Проходим по всем добавленным категориям
    for category_id in pk_set:
        try:
            category = Category.objects.get(id=category_id)
            
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
                    
                    # Формируем тему письма
                    subject = f'Новая запись в категории {category.name}: {instance.title}'
                    
                    # Создаем HTML сообщение
                    html_message = render_to_string('account/email/new_post_notification.html', {
                        'post': instance,
                        'user': subscriber,
                        'category': category,
                    })
                    
                    # Текстовая версия письма
                    text_message = f"""
Здравствуй, {subscriber.username}. Новая статья в твоём любимом разделе!

Заголовок: {instance.title}
Текст: {instance.text[:100]}...
Категория: {category.name}
Автор: {instance.author.user.username}
Дата: {instance.create_at.strftime('%d.%m.%Y %H:%M')}

Читать полностью: http://127.0.0.1:8000/news/{instance.id}/

---
Вы получили это письмо, потому что подписаны на категорию "{category.name}"
Управление подписками: http://127.0.0.1:8000/news/subscriptions/
                    """.strip()
                    
                    # Отправляем email
                    send_mail(
                        subject=subject,
                        message=text_message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[subscriber.email],
                        html_message=html_message,
                        fail_silently=True,  # Игнорируем ошибки отправки
                    )
                    
                except Exception:
                    # Игнорируем ошибки отправки отдельным подписчикам
                    pass
                    
        except Category.DoesNotExist:
            # Игнорируем несуществующие категории
            pass
        

@receiver(post_delete, sender=Post)
def send_delet_notifications(sender, instance, **kwargs):
    subject = f'{instance.title} has been deleted'
    mail_managers(
        subject=subject,
        message=f'Автор {instance.author.user.username} удалил свой пост!',
        fail_silently=True,
    )
