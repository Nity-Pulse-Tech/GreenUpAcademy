from django.db import router
from django.urls import path
from green_up_apps.admission.views.hors_ue_views import AdmissionView, HorsUeView

app_name = 'admission'

urlpatterns = [
    path('resident-hors-ue/', HorsUeView.as_view(), name='resident_hors_ue'),
    path('admission/', AdmissionView.as_view(), name='admission'),
]
