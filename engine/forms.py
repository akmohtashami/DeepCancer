from django import forms

from engine.models import ModelRun


class RequestRunForm(forms.ModelForm):
    class Meta:
        model = ModelRun
        fields = ["email", "input_file"]
