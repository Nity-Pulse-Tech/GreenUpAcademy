from django.db import router
from django.urls import path
from green_up_apps.formation.views.bachelor_views import (BachelorDesignerView, BachelorSecurityView, 
                                                          BachelorApplicationView, BachelorIndustryView)
from green_up_apps.formation.views.Mastère_professionnel_views import MasterDevelopmentView, MasterAiView

app_name = 'formation'

urlpatterns = [
    path('bachelor-designer/', BachelorDesignerView.as_view(), name='bachelor_designer'),
    path('bachelor-security/', BachelorSecurityView.as_view(), name='bachelor_security'),
    path('bachelor-application/', BachelorApplicationView.as_view(), name='bachelor_application'),
    path('bachelor-industry/', BachelorIndustryView.as_view(), name='bachelor_industry'),
    path('master-development/', MasterDevelopmentView.as_view(), name='master_development'),
    path('master-ai/', MasterAiView.as_view(), name='master_ai'),
]
