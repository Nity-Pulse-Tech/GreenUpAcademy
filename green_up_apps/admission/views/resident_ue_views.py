from django.views.generic import TemplateView
import logging

logger = logging.getLogger(__name__)

class ResidentUeView(TemplateView):
    template_name = "publics/home/admission/resident_ue/resident_ue.html"
    
    
class AdmissionUeView(TemplateView):
    template_name = "publics/home/admission/resident_ue/admission_process.html"