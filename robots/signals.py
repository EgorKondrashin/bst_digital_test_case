from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Robot
from orders.models import Order


@receiver(post_save, sender=Robot)
def notify_client(sender, instance, created, **kwargs):
    if created:
        orders = Order.objects.filter(robot_serial=instance.serial)
        for order in orders:
            send_mail(
                subject='Робот в наличии',
                message='Добрый день!\n'
                f'Недавно вы интересовались нашим роботом модели {instance.serial.split("-")[0]},'
                f'версии {instance.serial.split("-"[1])}.\n'
                f'Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами',
                from_email='from@example.com',
                recipient_list=[order.customer.email],
            )
