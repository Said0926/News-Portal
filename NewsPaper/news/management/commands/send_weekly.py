from django.core.management.base import BaseCommand
from news.tasks import send_weekly_digest

class Command(BaseCommand):
    help = 'Отправляет еженедельную рассылку подписчикам'
    
    def handle(self, *args, **options):
        send_weekly_digest()
        self.stdout.write('Рассылка отправлена')