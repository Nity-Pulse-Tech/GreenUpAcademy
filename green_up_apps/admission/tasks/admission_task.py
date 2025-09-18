import logging
from celery import shared_task
from django.utils.translation import gettext as _
from green_up_apps.users.models import User
from green_up_apps.global_data.email import EmailUtil
from green_up_apps.admission.models import EUAdmissionApplication, Program, Campus

logger = logging.getLogger(__name__)

@shared_task(name="notify_admission_pending")
def notify_admission_pending(application_id: str):
    """
    Task to notify admins when an EU admission application is marked 'PENDING'.
    """
    try:
        application = EUAdmissionApplication.objects.get(id=application_id)
        applicant = application.user
        program = application.program
        campus = application.campus

        # Get emails of active admins
        admin_emails = list(
            User.objects.filter(is_admin=True, is_active=True).values_list("email", flat=True)
        )

        email_util = EmailUtil(prod=True)

        # Notification to admins
        if admin_emails:
            email_util.send_email_with_template(
                template="publics/emails/admission_notification.html",
                context={
                    "is_admin": True,
                    "applicant_name": applicant.get_full_name(),
                    "program_name": program.name if program else "N/A",
                    "campus_name": campus.name if campus else "N/A",
                    "application_id": str(application.id),
                    "application_date": application.application_date.strftime("%Y-%m-%d %H:%M:%S"),
                },
                receivers=admin_emails,
                subject=_("New EU Admission Application Pending"),
            )
            logger.info(f"Notification sent to {len(admin_emails)} admin(s) for application {application_id}")

    except EUAdmissionApplication.DoesNotExist:
        logger.error(f"Application {application_id} not found for notification")
    except Exception as e:
        logger.error(f"Error sending admission notifications: {str(e)}", exc_info=True)