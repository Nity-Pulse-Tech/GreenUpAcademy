from celery import shared_task
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from green_up_apps.global_data.email import EmailUtil
import logging
from datetime import date
import time

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
    logger.info(f"Starting Celery task 'send_admission_emails' for application ID {application_id}")
    logger.debug(f"Task inputs: application_id={application_id}, user_data={user_data}, admin_emails={admin_emails}")
    
    # Use getattr to handle missing EMAIL_SENDING_ENABLED setting with default True
    email_sending_enabled = getattr(settings, 'EMAIL_SENDING_ENABLED', True)
    email_util = EmailUtil(prod=email_sending_enabled)
    
    # Logo path from settings
    logo_path = settings.LOGO
    inline_images = {"logo_image": logo_path}
    logger.debug(f"Using logo path: {logo_path}")
    
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
    logger.debug(f"Template context prepared: {context}")
    
    # 1. Send confirmation email to user
    user_email = user_data["email"]
    user_subject = _("Confirmation de réception de votre candidature - Green Up Academy")
    user_template = "publics/emails/admission_confirmation.html"
    
    logger.info(f"Attempting to send confirmation email to {user_email} for application ID {application_id}")
    start_time = time.time()
    try:
        success_user = email_util.send_email_with_template(
            template=user_template,
            context=context,
            receivers=[user_email],
            subject=user_subject,
            inline_images=inline_images
        )
        elapsed_time = time.time() - start_time
        if success_user:
            logger.info(f"Confirmation email sent successfully to {user_email} for application ID {application_id} in {elapsed_time:.2f} seconds")
        else:
            logger.error(f"Failed to send confirmation email to {user_email} for application ID {application_id} after {elapsed_time:.2f} seconds")
    except Exception as e:
        elapsed_time = time.time() - start_time
        logger.error(f"Exception while sending confirmation email to {user_email} for application ID {application_id} after {elapsed_time:.2f} seconds: {e}")
        success_user = False
    
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
    logger.debug(f"Admin email context: {context}")
    
    logger.info(f"Attempting to send admin notification email to {admin_emails} for application ID {application_id}")
    start_time = time.time()
    try:
        success_admin = email_util.send_email_with_template(
            template=admin_template,
            context=context,
            receivers=admin_emails,
            subject=admin_subject,
            inline_images=inline_images
        )
        elapsed_time = time.time() - start_time
        if success_admin:
            logger.info(f"Admin notification email sent successfully to {admin_emails} for application ID {application_id} in {elapsed_time:.2f} seconds")
        else:
            logger.error(f"Failed to send admin notification email to {admin_emails} for application ID {application_id} after {elapsed_time:.2f} seconds")
    except Exception as e:
        elapsed_time = time.time() - start_time
        logger.error(f"Exception while sending admin notification email to {admin_emails} for application ID {application_id} after {elapsed_time:.2f} seconds: {e}")
        success_admin = False
    
    logger.info(f"Completed Celery task 'send_admission_emails' for application ID {application_id}. User email success: {success_user}, Admin email success: {success_admin}")
    return success_user and success_admin