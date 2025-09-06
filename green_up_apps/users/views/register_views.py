from django.views.generic import TemplateView
import logging

logger = logging.getLogger(__name__)

class RegisterView(TemplateView):
    template_name = "publics/auth/register.html"