import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .forms import RobotForm


@method_decorator(csrf_exempt, name='dispatch')
class RobotCreateView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        form = RobotForm(data)
        if form.is_valid():
            robot = form.save()
            return JsonResponse({'status': 'success', 'data': {
                'serial': robot.serial,
                'model': robot.model,
                'version': robot.version,
                'created': robot.created
            }}, status=201)
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
