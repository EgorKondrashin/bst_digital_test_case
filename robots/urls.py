from django.urls import path
from .views import generate_exel_report

urlpatterns = [
    path('report/', generate_exel_report, name='generate-excel-report'),
]
