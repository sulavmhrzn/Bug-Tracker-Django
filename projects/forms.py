from django import forms
from tinymce.widgets import TinyMCE

from utils.constants import INPUT_CLASS, TEXTAREA_CLASS
from .models import Project


class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={**INPUT_CLASS}),
            "description": TinyMCE(attrs={**TEXTAREA_CLASS}),
        }
