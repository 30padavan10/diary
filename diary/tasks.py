# from diary.celery import app

# from .service import send
#
#
# @app.task       # данный декоратор и будет говорить celery что данная функция это таска и нужно ее отслеживать
# def send_spam_email(user_email):
#     send(user_email)