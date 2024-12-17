from django import forms
from django.core.exceptions import ValidationError

from .models import Robot


class RobotForm(forms.ModelForm):
    class Meta:
        model = Robot
        fields = ['model', 'version', 'created']

    def clean_model(self):
        model = self.cleaned_data['model']
        existing_models = Robot.objects.all()
        if model not in [existing_model.model for existing_model in existing_models]:
            raise ValidationError('Доступны модели соответствующие существующим в системе моделям.')

        return model
