from django import forms
from .models import Tasks

class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ('task_details','task_due_date','task_category','task_label')

class TaskUpdationForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ('task_details','task_due_date','task_category','task_label','task_status')


