from celery import Celery
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall1.settings")
app = Celery("celery_tasks")
# 加载celer中间人配置
app.config_from_object('celery_tasks.config')
# 检测任务
app.autodiscover_tasks(["celery_tasks.sms"])

from celery import Celery
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall1.settings")
app = Celery("celery_tasks")
# 检测任务
app.autodiscover_tasks(["celery_tasks.sms"])
# 加载celer中间人配置
app.config_from_object("celery_tasks.config")

