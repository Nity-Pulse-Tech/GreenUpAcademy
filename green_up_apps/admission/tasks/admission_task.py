import logging
from celery import shared_task
from django.utils.translation import gettext as _
from green_up_apps.users.models import User
from green_up_apps.global_data.email import EmailUtil
from green_up_apps.admission.models import EUAdmissionApplication, Program, Campus

logger = logging.getLogger(__name__)

@shared_task(name="green_up_apps.admission.tasks.admission_task.notify_admission_pending")
def notify_admission_pending(application_id: str):
    """
    Task to notify admins and the applicant when an EU admission application is marked 'PENDING'.
    """
    try:
        application = EUAdmissionApplication.objects.get(id=application_id)
        applicant = application.user
        program = application.program
        campus = application.campus

        # Common context for both emails
        context = {
            "applicant_name": applicant.get_full_name,
            "program_name": program.name if program else "N/A",
            "campus_name": campus.name if campus else "N/A",
            "application_id": str(application.id),
            "application_date": application.application_date.strftime("%Y-%m-%d %H:%M:%S"),
        }

        email_util = EmailUtil(prod=True)

        # Notification to admins
        admin_emails = list(
            User.objects.filter(is_admin=True, is_active=True).values_list("email", flat=True)
        )
        if admin_emails:
            email_util.send_email_with_template(
                template="publics/emails/admission_notification.html",
                context={**context, "is_admin": True},
                receivers=admin_emails,
                subject=_("New EU Admission Application Pending"),
            )
            logger.info(f"Notification sent to {len(admin_emails)} admin(s) for application {application_id}")

        # Notification to applicant
        if applicant.email:
            email_util.send_email_with_template(
                template="publics/emails/user_admission_confirmation.html",
                context={**context, "is_admin": False},
                receivers=[applicant.email],
                subject=_("Application Submission Confirmation"),
            )
            logger.info(f"Confirmation email sent to applicant {applicant.email} for application {application_id}")

    except EUAdmissionApplication.DoesNotExist:
        logger.error(f"Application {application_id} not found for notification")
    except Exception as e:
        logger.error(f"Error sending admission notifications: {str(e)}", exc_info=True)