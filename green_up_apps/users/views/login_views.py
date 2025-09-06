from django.views.generic import TemplateView
import logging

logger = logging.getLogger(__name__)

class LoginView(TemplateView):
    template_name = "publics/auth/login.html"