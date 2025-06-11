import os
from celery import Celery

# تنظیمات Django برای celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')

app = Celery('web')

# خواندن تنظیمات Celery از تنظیمات Django با پیشوند CELERY
app.config_from_object('django.conf:settings', namespace='CELERY')

# اتوماتیک کشف تسک‌ها از اپلیکیشن‌ها
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
