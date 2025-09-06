from django.db import router
from django.urls import path
from green_up_apps.users.views.contact_view import ContactView
from green_up_apps.users.views.home_views import HomeView
from green_up_apps.users.views.login_views import LoginView
from green_up_apps.users.views.logout_views import LogoutView
from green_up_apps.users.views.password_reset_views import PasswordResetRequestView, PasswordResetVerifyView, PasswordResetView
from green_up_apps.users.views.register_views import RegisterView, Verify2FAView


app_name = 'users'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-2fa/<str:email>/', Verify2FAView.as_view(), name='verify_2fa'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset/verify/<str:email>/', PasswordResetVerifyView.as_view(), name='password_reset_verify'),
    path('password-reset/reset/<str:email>/', PasswordResetView.as_view(), name='password_reset'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('contacts', ContactView.as_view(), name='contact'),
    
    
]
