import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from customers.models import Customer
from orders.models import Order
from robots.models import Robot


@method_decorator(csrf_exempt, name='dispatch')
class OrderCreateView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        email = data.get('email')
        model = data.get('model')
        version = data.get('version')

        if not email or not model or not version:
            return JsonResponse({'status': 'error', 'message': 'Неверно переданы данные'}, status=400)

        customer, created = Customer.objects.get_or_create(email=email)
        robot_serial = f'{model}-{version}'
        Order.objects.create(customer=customer, robot_serial=robot_serial)
        try:
            Robot.objects.filter(serial=robot_serial).exists()
            return JsonResponse({'status': 'success', 'message': 'Ваш заказ принят'}, status=201)
        except Robot.DoesNotExist:
            return JsonResponse({'status': 'success',
                                 'message': 'Мы оформим ваш заказ, но на данный момент такого робота у нас нет,'
                                            'если вы готовы подождать, мы с вами свяжемся как он появится'},
                                status=201)
