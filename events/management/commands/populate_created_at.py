from django.core.management.base import BaseCommand
from django.utils import timezone
from events.models import Event

class Command(BaseCommand):
    help = "Populate created_at field for existing records in Events"

    def handle(self, *args, **options):
        updated_count = Event.objects.all()
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {updated_count} records with created_at'))

