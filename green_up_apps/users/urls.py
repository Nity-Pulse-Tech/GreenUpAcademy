from django.db import router
from django.urls import path
from green_up_apps.users.views.contact_view import ContactView
from green_up_apps.users.views.home_views import HomeView
from green_up_apps.users.views.login_views import LoginView
from green_up_apps.users.views.register_views import RegisterView


app_name = 'users'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts', ContactView.as_view(), name='contact'),
    path('login', LoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    
]
