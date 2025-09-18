from celery import shared_task
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from green_up_apps.global_data.email import EmailUtil
import logging
from datetime import date

logger = logging.getLogger(__name__)

@shared_task
def send_admission_emails(application_id, user_data, admin_emails):
    """
    Celery task to send admission confirmation email to the user and notification to admins.
    
    Args:
        application_id (int): ID of the NonEUAdmissionApplication.
        user_data (dict): Dictionary containing user details (email, first_name, last_name, etc.).
        admin_emails (list): List of admin email addresses to notify.
    """
    email_util = EmailUtil(prod=settings.EMAIL_SENDING_ENABLED)
    
    # Logo path for inline image
    logo_path = f"{settings.BASE_DIR}/green_up_apps/static/images/logo.png"
    inline_images = {"logo_image": logo_path}
    
    # Prepare context for templates
    context = {
        "site_name": "Green Up Academy",
        "user_name": f"{user_data['first_name']} {user_data['last_name']}",
        "application_id": application_id,
        "program_name": user_data.get("program_name", "N/A"),
        "campus_name": user_data.get("campus_name", "N/A"),
        "season_name": user_data.get("season_name", "N/A"),
        "submission_date": date.today().strftime("%d %B %Y"),
    }
    
    # 1. Send confirmation email to user
    user_email = user_data["email"]
    user_subject = _("Confirmation de réception de votre candidature - Green Up Academy")
    user_template = "publics/emails/admission_confirmation.html"
    
    success_user = email_util.send_email_with_template(
        template=user_template,
        context=context,
        receivers=[user_email],
        subject=user_subject,
        inline_images=inline_images
    )
    
    if success_user:
        logger.info(f"Confirmation email sent to {user_email} for application ID {application_id}")
    else:
        logger.error(f"Failed to send confirmation email to {user_email} for application ID {application_id}")
    
    # 2. Send notification email to admins
    admin_subject = _("Nouvelle candidature reçue - Green Up Academy")
    admin_template = "publics/emails/admin_admission_notification.html"
    
    # Add user details to context for admin email
    context["user_details"] = {
        "first_name": user_data["first_name"],
        "last_name": user_data["last_name"],
        "email": user_data["email"],
        "phone_number": user_data.get("phone_number", "N/A"),
        "nationality": user_data.get("nationality", "N/A"),
        "date_of_birth": user_data.get("date_of_birth", "N/A"),
        "place_of_birth": user_data.get("place_of_birth", "N/A"),
        "passport_number": user_data.get("passport_number", "N/A"),
        "level_of_studies": user_data.get("level_of_studies", "N/A"),
        "address": user_data.get("address", "N/A"),
        "zip_code": user_data.get("zip_code", "N/A"),
        "city": user_data.get("city", "N/A"),
        "country": user_data.get("country", "N/A"),
    }
    
    success_admin = email_util.send_email_with_template(
        template=admin_template,
        context=context,
        receivers=admin_emails,
        subject=admin_subject,
        inline_images=inline_images
    )
    
    if success_admin:
        logger.info(f"Admin notification email sent for application ID {application_id}")
    else:
        logger.error(f"Failed to send admin notification email for application ID {application_id}")
    
    return success_user and success_admin