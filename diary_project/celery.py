import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diary_project.settings')  # указываем где находятся настройки джанго. Это
# делается для того чтобы прописать настройки CELERY в настройках джанго, и тогда celery будет их оттуда подхватывать,
# потому что в инструкции указано app = Celery('tasks', broker='pyamqp://guest@localhost//'), но т.к. у нас может быть
# много задач то так прописывать будет неудобно

app = Celery('diary_project')      # Создаем объект Celery и передаем ему имя
app.config_from_object('django.conf:settings', namespace='CELERY')  # с помощью данного метода из конфига настроек
# Celery будет подхватывать себе переменные которые начинаются на CELERY

app.autodiscover_tasks()    # автоматически подцеплять файлы с тасками

# не забыть добавить конфиг для Celery в __init__.py
# автоматически с запуском проекта Celery не запустится, нужно запускать отдельно worker

# celery -A diary worker -l info
# запусткать нужно из той же директории где manage.py
# diary - название которое передавали при создании app
# worker - то что хотим запустить воркер
# -l info - чтобы показывались логи


# celery beat
# выполнение периодических задач
#  для запуска шедулера нужно выполнять celery --workdir=./ -A diary_project beat --loglevel=info


app.conf.beat_schedule = {
    'send-spam-every-30-minute': {                       # название таски
        'task': 'diary.tasks.send_beat_email',
        'schedule': crontab(minute='*/30'),              # описание в документации celery Periodic Tasks
    },
}

# celery когда запускается в контейнере пишет SecurityWarning: You're running the worker with superuser privileges: this is
# diary_app_celery | absolutely not recommended!

# flower нужен когда много тасков, несколько воркеров. celery может запускаться на отдельном сервере
