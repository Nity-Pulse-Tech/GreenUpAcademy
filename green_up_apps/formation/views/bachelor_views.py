from django.views.generic import TemplateView
import logging

logger = logging.getLogger(__name__)

class BachelorDesignerView(TemplateView):
    template_name = "publics/home/formations/bachelor/bachelor_designer.html"
    
    
class BachelorSecurityView(TemplateView):
    template_name = "publics/home/formations/bachelor/bachelor_security.html"
    
class BachelorApplicationView(TemplateView):
    template_name = "publics/home/formations/bachelor/bachelor_application.html"
    
    
class BachelorIndustryView(TemplateView):
    template_name = "publics/home/formations/bachelor/bachelor_industry.html"