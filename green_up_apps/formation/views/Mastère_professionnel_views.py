from django.views.generic import TemplateView
import logging

logger = logging.getLogger(__name__)

class MasterDevelopmentView(TemplateView):
    template_name = "publics/home/formations/Mastère_professionnel/master_development.html"
    
    
class MasterAiView(TemplateView):
    template_name = "publics/home/formations/Mastère_professionnel/master_ai.html"