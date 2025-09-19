from django.core.management.base import BaseCommand
from green_up_apps.admission.models import Campus

class Command(BaseCommand):
    help = 'Populate the Campus model with default campuses'

    def handle(self, *args, **kwargs):
        campuses = ['Paris', 'Reims']
        for campus_name in campuses:
            campus, created = Campus.objects.get_or_create(name=campus_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created campus: {campus_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Campus already exists: {campus_name}'))