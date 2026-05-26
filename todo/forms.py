from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "content",
            "deadline",
            "tags",
        ]

        widgets = {
            "deadline": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "tags": forms.CheckboxSelectMultiple(
                attrs={"class": "form-check"}
            ),

        }
