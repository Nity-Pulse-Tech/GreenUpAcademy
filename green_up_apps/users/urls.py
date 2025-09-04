from django.db import router
from django.urls import path
from green_up_apps.users.views.contact_view import ContactView
from green_up_apps.users.views.home_views import HomeView


app_name = 'users'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts', ContactView.as_view(), name='contact'),
    
]
