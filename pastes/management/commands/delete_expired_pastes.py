from django.core.management.base import BaseCommand
from django.utils import timezone
from pastes.models import Paste

class Command(BaseCommand):
    help = 'Delete expired pastes'

    def handle(self, *args, **kwargs):
        current_time = timezone.now()
        expired_pastes = Paste.objects.filter(expires_at__lt=current_time)
        count = expired_pastes.count()
        expired_pastes.delete()
        
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} expired pastes'))
