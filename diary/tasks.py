from celery import shared_task
from django.core.mail import send_mail
import os
from diary_project.celery import app
from .models import Contact
from .service import send

@app.task       # данный декоратор и будет говорить celery что данная функция это таска и нужно ее отслеживать
def send_spam_email(user_email):
    send(user_email)

# при добавлении новой таски нужно всегда перезагружать celery

@app.task
def send_beat_email():
    for contact in Contact.objects.all():
        send_mail(
            'Вы подписались на рассылку новостей django',  # тема
            'Будет много интересного каждые 5 минут',  # текст письма
            os.getenv('NAME'),  # почта с которой отправлять
            [contact.email],  # почта на которую отправлять
            fail_silently=False,
        )

# можно тушить контейнер с воркером селери, при этом приложение продолжает работать и флауэр тоже работает и показывает что воркер офлайн
# чтобы проверить таски которые просто складывают числа, чтобы не создавать вьюхи воспользуемся консолью джанги:
# - заходим в контейнер приложения
# - в нем заходим в шел джанги
#
# >>> from diary.tasks import my_task
# >>> my_task.delay(2, 3)
# <AsyncResult: ca4dde52-1a29-4bf5-9364-16e0aeef0ce0>

# my_task.apply_async(countdown=60)  # вместо метода delay можно также использовать метод apply_async, они работают
# одинаково разница только немного в передаваемых аргументах. Отложенную таску можно вызывать без исключения

# >>> my_task.apply_async((5, 5), countdown=60)
# <AsyncResult: 684c34da-b25f-4407-95a6-ee6831936fd0>

@app.task
def my_task(a, b):
    c = a + b
    return c


@app.task
def my_task_as(d, e):
    c = d + e
    return c

# если таска упала, несмогла выполнить например подключение к бд и т.д. и выпало исключение, то повторяется таска
# по умолчанию через 3 минуты.

@app.task(bind=True, default_retry_delay=5 * 60) # можно указать здесь когда по умолч будет перезапуск. 60 - секунды
def my_task_retry(self, x, y):          # таски это классы
    try:
        return x + y
    except Exception as exc:            # можно в случае возникновения какого-то конкретного исключения вызывать
        raise self.retry(exc=exc, countdown=60) # перезапуск, указывать через сколь здесь countdown


# shared_task и app.task это одинаковые таски, но app.task мы используем когда у нас есть проект например джанго и мы
# там создаем app который связан с джанго, то shared_task можно использовать когда у нас какой-то независимый от
# проекта скрипт или модуль который переносим

@shared_task()
def my_sh_task(msg):
    return msg + "!!!"


# таска может вызывать саму себя с новым аргументом. Поведение следующее: вызывается таска и считает 5+5 и потом
# вызывается эта же таска и считаются аргументы как 10+20

# >>> my_task.apply_async((5, 5), link=my_task.s(20))
# <AsyncResult: a41e18ad-d011-405b-ba52-b23ecfba1506>


# Как таски хранятся в redis:

# заходим в контейнер


# redis-cli INFO keyspace - показывает количество ключей в базах редис

# root@08a8a9546a05:/data# redis-cli

# 127.0.0.1:6379> keys *
#  1) "_kombu.binding.celeryev"
#  2) "celery-task-meta-a41e18ad-d011-405b-ba52-b23ecfba1506"
#  3) "celery-task-meta-ca4dde52-1a29-4bf5-9364-16e0aeef0ce0"
#  4) "celery-task-meta-0ea04778-b87a-49cd-aa12-910dbf3afeed"
#  5) "celery-task-meta-966f3f57-0152-4637-996e-ef7e98a29e2c"
#  6) "_kombu.binding.celery"
#  7) "celery-task-meta-a68c9f64-ab30-4b50-8d16-9243a232aa45"
#  8) "celery-task-meta-8425651e-8067-4466-a27c-9c99088e14a5"
#  9) "celery-task-meta-684c34da-b25f-4407-95a6-ee6831936fd0"
# 10) "_kombu.binding.celery.pidbox"

# 127.0.0.1:6379> get celery-task-meta-ca4dde52-1a29-4bf5-9364-16e0aeef0ce0
# "{\"status\": \"SUCCESS\", \"result\": 5, \"traceback\": null, \"children\": [], \"date_done\": \"2022-06-25T20:47:41.348095\", \"task_id\": \"ca4dde52-1a29-4bf5-9364-16e0aeef0ce0\"}"

