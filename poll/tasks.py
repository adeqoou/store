from celery import shared_task
from django.core.mail import send_mail
from users.models import Contact


@shared_task
def email_send(user_email):
    send_mail(
        'Интернет - магазин',
         f'Почта/ Посетите наш сайт: http://127.0.0.1:8000/',
        'aidarbekovadahan8@gmail.com',
        [user_email],
        fail_silently=False
    )


@shared_task()
def send_beat_email():
    for contact in Contact.objects.all():
        send_mail(
            'Интернет-магазин',
            'Мы будем отправлять вам сообщения каждые 5 минут',
            'aidarbekovadahan8@gmail.com',
            [contact.email],
            fail_silently=False
        )