from django.views.generic import TemplateView
import logging

logger = logging.getLogger(__name__)

class HorsUeView(TemplateView):
    template_name = "publics/home/admission/resident_hor_ue.html"