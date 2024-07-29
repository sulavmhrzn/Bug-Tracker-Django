from django import forms
from tinymce.widgets import TinyMCE

from accounts.models import User
from projects.models import Project
from utils.constants import INPUT_CLASS, TEXTAREA_CLASS, SELECT_CLASS
from .models import Bug, Comment


class CreateBugForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CreateBugForm, self).__init__(*args, **kwargs)

        self.fields["project"].queryset = Project.objects.filter(manager=user)
        self.fields["assigned_to"].queryset = User.objects.filter(
            role=User.ROLE.DEVELOPER
        )

    class Meta:
        model = Bug
        fields = "__all__"
        labels = {"assigned_to": "Assign to"}
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Login Filed", **INPUT_CLASS}
            ),
            "description": TinyMCE(attrs=TEXTAREA_CLASS),
            "project": forms.Select(attrs=SELECT_CLASS),
            "assigned_to": forms.Select(attrs=SELECT_CLASS),
            "priority": forms.Select(attrs=SELECT_CLASS),
            "status": forms.Select(attrs=SELECT_CLASS),
        }

    def _post_clean(self):
        super()._post_clean()
        for k, v in self.errors.items():
            if self.fields[k].widget.__class__.__name__ == "Select":
                self.fields[k].widget.attrs["class"] += " select-error"
            if self.fields[k].widget.__class__.__name__ == "TextInput":
                self.fields[k].widget.attrs["class"] += " input-error"
            if self.fields[k].widget.__class__.__name__ == "Textarea":
                self.fields[k].widget.attrs["class"] += " textarea-error"


class UpdateBugLifecycleForm(forms.ModelForm):
    class Meta:
        model = Bug
        fields = ["status", "priority"]
        widgets = {
            "status": forms.Select(attrs=INPUT_CLASS),
            "priority": forms.Select(attrs=INPUT_CLASS),
        }


class BugFilterForm(forms.Form):
    project = forms.ModelChoiceField(
        required=False,
        queryset=Project.objects.all(),
        widget=forms.Select(attrs=INPUT_CLASS),
    )
    priority = forms.ChoiceField(
        required=False,
        choices=[("", ""), ("L", "Low"), ("M", "Medium"), ("H", "High")],
        widget=forms.Select(attrs=INPUT_CLASS),
    )
    status = forms.ChoiceField(
        required=False,
        choices=[("", ""), ("I", "In progress"), ("O", "Open"), ("C", "Closed")],
        widget=forms.Select(attrs=INPUT_CLASS),
    )


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["description"]
        widgets = {"description": forms.Textarea(attrs=TEXTAREA_CLASS)}
