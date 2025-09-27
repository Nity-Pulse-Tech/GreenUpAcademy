import logging
from django.views.generic import View, TemplateView
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from green_up_apps.admission.models import EUAdmissionApplication, Program, Campus, Diploma, AdmissionSeason
from green_up_apps.users.models import User, Profile
from green_up_apps.global_data.enums import ApplicationStatusChoices, ApprenticeshipChoices, ProgramLevelChoices
# from green_up_apps.admission.tasks.admission_task import notify_admission_pending

logger = logging.getLogger(__name__)

class ResidentUeView(TemplateView):
    template_name = "publics/home/admission/resident_ue/resident_ue.html"
    
class AdmissionUeView(View):
    """View for handling EU admission application form submission"""

    def get(self, request):
        context = {
            'campuses': Campus.objects.all(),
            'bachelor_programs': Program.objects.filter(level=ProgramLevelChoices.BACHELOR),
            'master_programs': Program.objects.filter(level=ProgramLevelChoices.MASTER),
            'apprenticeship_choices': ApprenticeshipChoices.choices,
        }
        return TemplateView.as_view(
            template_name="publics/home/admission/resident_ue/admission_process.html",
            extra_context=context
        )(request)

    def post(self, request):
        try:
            
            from green_up_apps.admission.tasks.admission_task import notify_admission_pending
            # Extract form data
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            date_of_birth = request.POST.get('date_of_birth')
            phone_number = request.POST.get('phone_number')
            address = request.POST.get('address')
            zip_code = request.POST.get('zip_code')
            city = request.POST.get('city')
            country = request.POST.get('country')
            last_diploma = request.POST.get('last_diploma')
            institution = request.POST.get('institution')
            institution_city_country = request.POST.get('institution_city_country')
            year_obtained = request.POST.get('year_obtained')
            campus_name = request.POST.get('campus')
            program_name = request.POST.get('program')
            apprenticeship_status = request.POST.get('apprenticeship')
            declaration_place = request.POST.get('declaration_place')
            declaration_date = request.POST.get('declaration_date')
            how_heard = {
                'internet': request.POST.get('how_heard_internet') == 'on',
                'social_media': request.POST.get('how_heard_social_media') == 'on',
                'forum': request.POST.get('how_heard_forum'),
                'student_alumni': request.POST.get('how_heard_student_alumni') == 'on',
                'other': request.POST.get('how_heard_other'),
            }
            declaration_accepted = request.POST.get('declaration_accepted') == 'on'

            # File uploads
            cv = request.FILES.get('cv')
            motivation_letter = request.FILES.get('lettre_motivation')
            academic_records = request.FILES.get('releves_notes')
            identity_document = request.FILES.get('piece_identite')
            photo = request.FILES.get('photo_identite')
            portfolio = request.FILES.get('portfolio')
            signature = request.FILES.get('signature')

            # Log received data for debugging
            logger.debug(f"Received apprenticeship_status: {apprenticeship_status}")
            logger.debug(f"Form data: {request.POST}")
            logger.debug(f"Files: {request.FILES}")

            # Validate required fields
            required_fields = [
                first_name, last_name, email, date_of_birth, phone_number, address,
                zip_code, city, country, last_diploma, institution, institution_city_country,
                year_obtained, campus_name, program_name, declaration_place, declaration_date,
                cv, motivation_letter, academic_records, identity_document, photo, signature
            ]
            if not all(required_fields) or not declaration_accepted:
                logger.warning(f'Missing required fields in EU admission application by user {request.user.id}')
                return JsonResponse({
                    'success': False,
                    'message': _('Please fill in all required fields and accept the declaration.')
                }, status=400)

            # Validate apprenticeship status
            if apprenticeship_status not in dict(ApprenticeshipChoices.choices):
                logger.warning(f'Invalid apprenticeship status provided: {apprenticeship_status}')
                return JsonResponse({
                    'success': False,
                    'message': _('The selected apprenticeship status is invalid.')
                }, status=400)

            # Validate program and campus
            try:
                program = Program.objects.get(name=program_name)
            except Program.DoesNotExist:
                logger.error(f'Program not found: {program_name}')
                return JsonResponse({
                    'success': False,
                    'message': _('The selected program does not exist.')
                }, status=404)

            try:
                campus = Campus.objects.get(name=campus_name)
            except Campus.DoesNotExist:
                logger.error(f'Campus not found: {campus_name}')
                return JsonResponse({
                    'success': False,
                    'message': _('The selected campus does not exist.')
                }, status=404)

            # Validate program-campus relationship
            if not program.campuses.filter(id=campus.id).exists():
                logger.warning(f'Program {program_name} not offered at campus {campus_name}')
                return JsonResponse({
                    'success': False,
                    'message': _('The selected program is not offered at the chosen campus.')
                }, status=400)

            # Validate admission season
            season = AdmissionSeason.objects.filter(is_active=True).first()
            if not season:
                logger.error('No active admission season found')
                return JsonResponse({
                    'success': False,
                    'message': _('No active admission season is available. Please contact support.')
                }, status=400)

            # Update or create user and profile
            user = request.user
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()

            profile, created = Profile.objects.get_or_create(user=user)
            profile.phone_number = phone_number
            profile.address = address
            profile.zip_code = zip_code
            profile.city = city
            profile.country = country
            profile.save()

            # Create or update diploma
            diploma, created = Diploma.objects.get_or_create(
                user=user,
                name=last_diploma,
                defaults={
                    'institution': institution,
                    'city_country': institution_city_country,
                    'year': year_obtained
                }
            )

            # Create admission application
            application = EUAdmissionApplication(
                user=user,
                season=season,
                civility=request.POST.get('civility', ''),
                date_of_birth=date_of_birth,
                program=program,
                campus=campus,
                cv=cv,
                motivation_letter=motivation_letter,
                academic_records=academic_records,
                identity_document=identity_document,
                photo=photo,
                portfolio=portfolio,
                signature=signature,
                last_diploma=last_diploma,
                institution=institution,
                institution_city_country=institution_city_country,
                year_obtained=year_obtained,
                apprenticeship_status=apprenticeship_status,
                registration_fee=1200.00,
                declaration_place=declaration_place,
                declaration_date=declaration_date,
                declaration_accepted=declaration_accepted,
                how_heard=how_heard,
                status=ApplicationStatusChoices.PENDING
            )
            application.save()
            application.diplomas.add(diploma)

            # Trigger Celery task for admin notification
            if application.status == ApplicationStatusChoices.PENDING:
                notify_admission_pending.delay(str(application.id))

            logger.info(f'EU Admission application created by user {request.user.id}: {application.id}')
            return JsonResponse({
                'success': True,
                'data': {
                    'id': str(application.id),
                },
                'message': _('Application submitted successfully.')
            }, status=201)

        except Exception as e:
            logger.error(f'Unexpected error during EU admission application creation: {str(e)}', exc_info=True)
            return JsonResponse({
                'success': False,
                'message': _('An unexpected error occurred while submitting the application. Please try again.')
            }, status=500)