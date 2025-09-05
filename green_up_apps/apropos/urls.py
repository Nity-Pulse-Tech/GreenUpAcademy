from django.db import router
from django.urls import path
from green_up_apps.apropos.views.notre_equip_views import NotreEquipeView, ReglementView

app_name = 'apropos'

urlpatterns = [
    path('equipe/', NotreEquipeView.as_view(), name='notre_equipe'),
    path('reglement/', ReglementView.as_view(), name='reglement'),
]
