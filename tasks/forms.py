from django import forms
from django.forms import ModelForm, Textarea, DateInput
from .models import Tasks, Labels

class TaskCreationForm(forms.ModelForm):
    task_category = forms.CharField(required=False)
    task_label = forms.CharField(required=False)
    class Meta:
        model = Tasks
        fields = ('task_details','task_due_date','task_category','task_label')
        widgets = {'task_details': Textarea(attrs={'cols': 40, 'rows': 5}),'task_due_date': DateInput()}

class TaskUpdationForm(forms.ModelForm):
    task_category = forms.CharField(required=False)
    task_label = forms.CharField(required=False)
    class Meta:
        model = Tasks
        fields = ('task_details','task_due_date','task_category','task_label','task_status')
        widgets = {'task_details': Textarea(attrs={'cols': 40, 'rows': 5}),'task_due_date': DateInput()}

class LabelCreationForm(forms.ModelForm):
    class Meta:
        model = Labels
        fields = ('label_name',)

