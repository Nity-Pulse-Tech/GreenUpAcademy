from django.core.management.base import BaseCommand
from green_up_apps.admission.models import Program, Campus
from green_up_apps.global_data.enums import ProgramLevelChoices

class Command(BaseCommand):
    help = 'Populate the Program model with default programs'

    def handle(self, *args, **kwargs):
        programs = [
            {
                'name': "Conception et Développement d'Application",
                'level': ProgramLevelChoices.BACHELOR,
                'tuition_fee': 5000.00
            },
            {
                'name': 'Intelligence Artificielle',
                'level': ProgramLevelChoices.BACHELOR,
                'tuition_fee': 5000.00
            },
            {
                'name': "Administrateur d'Infrastructure Sécurisée",
                'level': ProgramLevelChoices.BACHELOR,
                'tuition_fee': 5000.00
            },
            {
                'name': 'Performance Énergétique des Bâtiments et Procédés Industriels',
                'level': ProgramLevelChoices.BACHELOR,
                'tuition_fee': 5000.00
            },
            {
                'name': 'Conception Designer UI',
                'level': ProgramLevelChoices.BACHELOR,
                'tuition_fee': 5000.00
            },
            {
                'name': 'Performance Énergétique, Intelligence Artificielle & Développement Durable',
                'level': ProgramLevelChoices.MASTER,
                'tuition_fee': 7000.00
            },
            {
                'name': 'Intelligence Artificielle',
                'level': ProgramLevelChoices.MASTER,
                'tuition_fee': 7000.00
            },
        ]

        # Ensure campuses 'Paris' and 'Reims' exist
        try:
            paris = Campus.objects.get(name='Paris')
            reims = Campus.objects.get(name='Reims')
        except Campus.DoesNotExist:
            self.stdout.write(self.style.ERROR('Campuses "Paris" and "Reims" must exist. Run "populate_campuses" first.'))
            return

        for program_data in programs:
            program, created = Program.objects.get_or_create(
                name=program_data['name'],
                defaults={
                    'level': program_data['level'],
                    'tuition_fee': program_data['tuition_fee']
                }
            )
            if created:
                program.campuses.add(paris, reims)
                self.stdout.write(self.style.SUCCESS(f'Created program: {program.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Program already exists: {program.name}'))