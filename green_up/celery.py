import os
import django
from celery import Celery
from decouple import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "green_up.settings")

app = Celery("green_up")

# Load settings from Django
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks in installed apps
app.autodiscover_tasks()
# Set the default Django settings module for the Celery worker
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'green_up.settings')
django.setup()  # Initialize Django settings

# Read broker and backend URLs from environment variables
broker_url = config('CELERY_BROKER_URL', default='redis://localhost:6379/3')
backend_url = config('CELERY_RESULT_BACKEND', default='redis://localhost:6379/3')

app = Celery(
    'green_up',
    broker=broker_url,
    backend=backend_url,
    include=['green_up_apps.admission.tasks.send_admission_emails']
)

# Celery configuration
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

app.autodiscover_tasks()
