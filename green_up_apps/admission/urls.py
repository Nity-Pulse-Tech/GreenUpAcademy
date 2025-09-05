from django.db import router
from django.urls import path
from green_up_apps.admission.views.hors_ue_views import AdmissionView, HorsUeView
from green_up_apps.admission.views.resident_ue_views import AdmissionUeView, ResidentUeView

app_name = 'admission'

urlpatterns = [
    path('resident-hors-ue/', HorsUeView.as_view(), name='resident_hors_ue'),
    path('admission/', AdmissionView.as_view(), name='admission'),
    path('resident-ue/', ResidentUeView.as_view(), name='resident_ue'),
    path('admission-ue/', AdmissionUeView.as_view(), name='admission_ue'),
]
