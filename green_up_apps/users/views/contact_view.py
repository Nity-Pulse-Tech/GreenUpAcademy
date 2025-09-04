from django.views.generic import TemplateView
import logging

logger = logging.getLogger(__name__)

class ContactView(TemplateView):
    template_name = "publics/home/contact/contact.html"