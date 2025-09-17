from celery import Celery

app = Celery('green_up', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

# Optional: Load tasks from all registered apps
app.autodiscover_tasks()