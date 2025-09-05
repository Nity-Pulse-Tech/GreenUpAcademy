from django.views.generic import TemplateView
import logging

logger = logging.getLogger(__name__)

class NotreEquipeView(TemplateView):
    template_name = "publics/home/apropos/notre_equipe.html"
    
    
class ReglementView(TemplateView):
    template_name = "publics/home/apropos/reglement.html"