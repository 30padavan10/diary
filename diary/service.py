from django.core.mail import send_mail

from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent

from dotenv import load_dotenv
dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)


def send(user_email):
    """Выполняет стандартную функцию django по отправке писем"""
    send_mail(
        'Вы подписались на рассылку новостей django',   # тема
        'Будет много интересного',                      # текст письма
        os.getenv('NAME'),                             # почта с которой отправлять
        [user_email],                                   # почта на которую отправлять
        fail_silently=False,
    )