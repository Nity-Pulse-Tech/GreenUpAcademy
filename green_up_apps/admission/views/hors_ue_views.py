import logging
from django.views.generic import View
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.core.validators import FileExtensionValidator
from green_up_apps.admission.models import NonEUAdmissionApplication, Program, Campus, Diploma, AdmissionSeason
from green_up_apps.global_data.enums import ApplicationStatusChoices, CivilityChoices
# from green_up_apps.admission.tasks.send_admission_emails import send_admission_emails

# Set up logging
logger = logging.getLogger(__name__)

class NonEUAdmissionApplicationView(View):
    template_name = 'publics/home/admission/resident_hors/admission_process.html'
    success_url = reverse_lazy('admission:non_eu_admission_success')

    def get(self, request, *args, **kwargs):
        """Render the admission form with pre-filled user/profile data and open seasons."""
        open_seasons = [season for season in AdmissionSeason.objects.filter(is_active=True) if season.is_open()]
        context = {
            'programs': Program.objects.all(),
            'campuses': Campus.objects.all(),
            'civility_choices': CivilityChoices.choices,
            'seasons': open_seasons,
        }
        if not open_seasons:
            logger.warning("No open admission seasons available.")
            messages.error(request, _("Aucune session d'admission ouverte n'est disponible actuellement."))
            return HttpResponseRedirect(reverse_lazy('home'))

        if request.user.is_authenticated:
            user = request.user
            profile = getattr(user, 'profile', None)
            context['user_data'] = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone_number': profile.phone_number if profile else '',
                'address': profile.address if profile else '',
                'zip_code': profile.zip_code if profile else '',
                'city': profile.city if profile else '',
                'country': profile.country if profile else '',
            }
        logger.debug(f"Rendering admission form for user {request.user.email if request.user.is_authenticated else 'anonymous'}")
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        try:
            
            from green_up_apps.admission.tasks.send_admission_emails import send_admission_emails
            # Ensure user is authenticated
            if not request.user.is_authenticated:
                logger.error("Unauthenticated user attempted to submit non-EU admission application.")
                messages.error(request, _("Vous devez être connecté pour soumettre une candidature."))
                return HttpResponseRedirect(self.request.path)

            user = request.user
            post_data = request.POST
            files = request.FILES
            logger.debug(f"Processing POST data for user {user.email}: {post_data.keys()}")

            # Validate required fields
            required_fields = [
                'first_name', 'last_name', 'email', 'date_of_birth', 'phone_number',
                'address', 'zip_code', 'city', 'country', 'place_of_birth',
                'nationality', 'passport_number', 'level_of_studies',
                'program', 'campus', 'cv', 'motivation_letter',
                'identity_document', 'photo', 'academic_records',
                'declaration_accepted', 'season'
            ]
            for field in required_fields:
                if field not in post_data and field not in files:
                    logger.error(f"Missing required field {field} for user {user.email}")
                    messages.error(request, _(f"Champ requis manquant : {field}"))
                    return HttpResponseRedirect(self.request.path)

            # Validate season
            try:
                season = AdmissionSeason.objects.get(id=post_data['season'])
                if not season.is_open():
                    logger.error(f"Selected season {season.name} is not open for user {user.email}")
                    messages.error(request, _("La session sélectionnée n'est pas ouverte aux candidatures."))
                    return HttpResponseRedirect(self.request.path)
            except AdmissionSeason.DoesNotExist:
                logger.error(f"Invalid season selected by user {user.email}: {post_data['season']}")
                messages.error(request, _("Session d'admission invalide."))
                return HttpResponseRedirect(self.request.path)

            # Validate file extensions
            file_validator = FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])
            for file_field in ['cv', 'motivation_letter', 'identity_document', 'academic_records', 'language_certificate']:
                if file_field in files:
                    try:
                        file_validator(files[file_field])
                    except ValidationError as e:
                        logger.error(f"Invalid file extension for {file_field} by user {user.email}: {e}")
                        messages.error(request, _(f"Format de fichier invalide pour {file_field}. Formats autorisés : PDF, JPG, JPEG, PNG."))
                        return HttpResponseRedirect(self.request.path)

            # Validate photo separately (only jpg, jpeg, png)
            if 'photo' in files:
                try:
                    FileExtensionValidator(['jpg', 'jpeg', 'png'])(files['photo'])
                except ValidationError as e:
                    logger.error(f"Invalid file extension for photo by user {user.email}: {e}")
                    messages.error(request, _("Format de fichier invalide pour la photo. Formats autorisés : JPG, JPEG, PNG."))
                    return HttpResponseRedirect(self.request.path)

            # Validate program and campus
            try:
                program = Program.objects.get(id=post_data['program'])
                campus = Campus.objects.get(id=post_data['campus'])
            except (Program.DoesNotExist, Campus.DoesNotExist) as e:
                logger.error(f"Invalid program or campus selected by user {user.email}: {e}")
                messages.error(request, _("Programme ou campus sélectionné invalide."))
                return HttpResponseRedirect(self.request.path)

            # Validate civility
            if post_data.get('civility') not in [choice[0] for choice in CivilityChoices.choices]:
                logger.error(f"Invalid civility value provided by user {user.email}: {post_data.get('civility')}")
                messages.error(request, _("Valeur de civilité invalide."))
                return HttpResponseRedirect(self.request.path)

            # Validate declaration accepted
            if post_data.get('declaration_accepted') != 'on':
                logger.error(f"Declaration not accepted by user {user.email}")
                messages.error(request, _("Vous devez accepter la déclaration pour soumettre la candidature."))
                return HttpResponseRedirect(self.request.path)

            # Process how_heard
            how_heard = []
            for source in ['internet', 'fair', 'word_of_mouth', 'gua_student', 'press', 'other']:
                if post_data.get(source) == 'on':
                    how_heard.append(source)
            how_heard_json = {'sources': how_heard}
            logger.debug(f"How heard sources for user {user.email}: {how_heard}")

            # Process multiple diplomas
            diplomas = []
            i = 0
            while f'diploma_name_{i}' in post_data:
                try:
                    diploma_data = {
                        'name': post_data[f'diploma_name_{i}'],
                        'institution': post_data[f'institution_{i}'],
                        'city_country': post_data[f'city_country_{i}'],
                        'year': post_data[f'year_{i}']
                    }
                    if all(diploma_data.values()):
                        diploma = Diploma(
                            user=user,
                            name=diploma_data['name'],
                            institution=diploma_data['institution'],
                            city_country=diploma_data['city_country'],
                            year=diploma_data['year']
                        )
                        diplomas.append(diploma)
                    else:
                        logger.warning(f"Incomplete diploma data at index {i} for user {user.email}: {diploma_data}")
                        messages.error(request, _(f"Données incomplètes pour le diplôme {i + 1}. Tous les champs sont requis."))
                        return HttpResponseRedirect(self.request.path)
                except Exception as e:
                    logger.error(f"Error processing diploma {i} for user {user.email}: {e}")
                    messages.error(request, _(f"Erreur lors du traitement du diplôme {i + 1}."))
                    return HttpResponseRedirect(self.request.path)
                i += 1

            if not diplomas:
                logger.error(f"No valid diplomas provided by user {user.email}")
                messages.error(request, _("Au moins un diplôme valide est requis."))
                return HttpResponseRedirect(self.request.path)

            # Update User and Profile
            form_data = {
                'first_name': post_data['first_name'],
                'last_name': post_data['last_name'],
                'email': post_data['email'],
                'phone_number': post_data['phone_number'],
                'address': post_data['address'],
                'zip_code': post_data['zip_code'],
                'city': post_data['city'],
                'country': post_data['country']
            }
            try:
                application = NonEUAdmissionApplication(user=user)
                application.update_user_and_profile(form_data)
                logger.debug(f"User profile updated for {user.email}: {form_data}")
            except Exception as e:
                logger.error(f"Error updating user/profile for {user.email}: {e}")
                messages.error(request, _("Erreur lors de la mise à jour du profil utilisateur."))
                return HttpResponseRedirect(self.request.path)

            # Create application
            application = NonEUAdmissionApplication(
                user=user,
                season=season,
                civility=post_data.get('civility', ''),
                date_of_birth=post_data['date_of_birth'],
                program=program,
                campus=campus,
                cv=files.get('cv'),
                motivation_letter=files.get('motivation_letter'),
                portfolio=files.get('portfolio'),
                identity_document=files.get('identity_document'),
                photo=files.get('photo'),
                academic_records=files.get('academic_records'),
                declaration_accepted=True,
                how_heard=how_heard_json,
                status=ApplicationStatusChoices.PENDING,
                place_of_birth=post_data['place_of_birth'],
                nationality=post_data['nationality'],
                passport_number=post_data['passport_number'],
                level_of_studies=post_data['level_of_studies'],
                language_certificate=files.get('language_certificate'),
                parent_last_name=post_data.get('parent_last_name'),
                parent_first_name=post_data.get('parent_first_name'),
                parent_phone_number=post_data.get('parent_phone_number'),
                parent_email=post_data.get('parent_email'),
                parent_address=post_data.get('parent_address'),
                parent_postal_code=post_data.get('parent_postal_code'),
                parent_city=post_data.get('parent_city'),
                parent_country=post_data.get('parent_country')
            )

            # Save application and diplomas
            try:
                application.save()
                for diploma in diplomas:
                    diploma.save()
                    application.diplomas.add(diploma)
                
                # Prepare user data for email
                user_data = {
                    'first_name': post_data['first_name'],
                    'last_name': post_data['last_name'],
                    'email': post_data['email'],
                    'phone_number': post_data['phone_number'],
                    'address': post_data['address'],
                    'zip_code': post_data['zip_code'],
                    'city': post_data['city'],
                    'country': post_data['country'],
                    'nationality': post_data['nationality'],
                    'date_of_birth': post_data['date_of_birth'],
                    'place_of_birth': post_data['place_of_birth'],
                    'passport_number': post_data['passport_number'],
                    'level_of_studies': post_data['level_of_studies'],
                    'program_name': program.name,
                    'campus_name': campus.name,
                    'season_name': season.name,
                }
                
                # Trigger Celery task to send emails
                admin_emails = ["fotsoeddysteve@gmail.com"]
                logger.info(f"Triggering Celery task 'send_admission_emails' for application ID {application.id}, user {user.email}, admin emails {admin_emails}")
                try:
                    send_admission_emails.delay(application.id, user_data, admin_emails)
                    logger.debug(f"Celery task 'send_admission_emails' dispatched successfully for application ID {application.id}")
                except Exception as e:
                    logger.error(f"Failed to dispatch Celery task 'send_admission_emails' for application ID {application.id}: {e}")
                
                logger.info(f"Non-EU admission application submitted successfully by {user.email} for season {season.name}")
                messages.success(request, _("Candidature soumise avec succès ! Vous recevrez une confirmation par e-mail."))
                return HttpResponseRedirect(self.success_url)
            except ValidationError as e:
                logger.error(f"Validation error saving application for {user.email}: {e}")
                messages.error(request, _("Erreur lors de l'enregistrement de la candidature : ") + str(e))
                return HttpResponseRedirect(self.request.path)
            except Exception as e:
                logger.error(f"Unexpected error saving application for {user.email}: {e}")
                messages.error(request, _("Une erreur inattendue s'est produite. Veuillez réessayer."))
                return HttpResponseRedirect(self.request.path)

        except Exception as e:
            logger.error(f"Unexpected error processing non-EU admission application for {request.user.email if request.user.is_authenticated else 'anonymous'}: {e}")
            messages.error(request, _("Une erreur inattendue s'est produite. Veuillez contacter le support."))
            return HttpResponseRedirect(self.request.path)