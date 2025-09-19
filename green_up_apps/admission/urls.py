from django.urls import path
from green_up_apps.admission.views.hors_ue_views import NonEUAdmissionApplicationView, ResidentHorsUeView
from green_up_apps.admission.views.resident_ue_views import AdmissionUeView, ResidentUeView
from django.views.generic import TemplateView

app_name = 'admission'

urlpatterns = [
    path('admission-hors-ue/', NonEUAdmissionApplicationView.as_view(), name='admission_hors_ue'),
    path('resident-hors-ue/success/', TemplateView.as_view(template_name='publics/home/admission/resident_hors/success.html'), name='non_eu_admission_success'),
    path('resident-ue/', ResidentUeView.as_view(), name='resident_ue'),
    path('resident-hors-ue/', ResidentHorsUeView.as_view(), name='resident_hors_ue'),
    path('admission-ue/', AdmissionUeView.as_view(), name='admission_ue'),
]