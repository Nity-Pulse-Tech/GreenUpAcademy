import os
from celery import Celery
from decouple import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "green_up.settings")

app = Celery("green_up")

# Load settings from Django
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks in installed apps
app.autodiscover_tasks()

# Read broker and backend URLs from environment variables
broker_url = config("CELERY_BROKER_URL", default="redis://localhost:6379/3")
backend_url = config("CELERY_RESULT_BACKEND", default="redis://localhost:6379/3")

app.conf.update(
    broker_url=broker_url,
    result_backend=backend_url,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
