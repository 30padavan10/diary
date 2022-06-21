import os
# from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diary_project.settings')  # указываем где находятся настройки джанго. Это
# делается для того чтобы прописать настройки CELERY в настройках джанго, и тогда celery будет их оттуда подхватывать,
# потому что в инструкции указано app = Celery('tasks', broker='pyamqp://guest@localhost//'), но т.к. у нас может быть
# много задач то так прописывать будет неудобно

# app = Celery('diary')      # Создаем объект Celery и передаем ему имя
# app.config_from_object('django.conf:settings', namespace='CELERY')  # с помощью данного метода из конфига настроек
# Celery будет подхватывать себе переменные которые начинаются на CELERY

# app.autodiscover_tasks()    # автоматически подцеплять файлы с тасками

# не забыть добавить конфиг для Celery в __init__.py
# автоматически с запуском проекта Celery не запустится, нужно запускать отдельно worker

# celery -A diary worker -l info
# запусткать нужно из той же директории где manage.py
# diary - название которое передавали при создании app
# worker - то что хотим запустить воркер
# -l info - чтобы показывались логи