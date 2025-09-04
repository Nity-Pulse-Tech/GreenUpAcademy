from django.db import router
from django.urls import path
from green_up_apps.admission.views.hors_ue_views import HorsUeView

app_name = 'admission'

urlpatterns = [
    path('resident-hors-ue/', HorsUeView.as_view(), name='resident_hors_ue'),
]
