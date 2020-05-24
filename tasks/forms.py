from django import forms
from django.forms import ModelForm, Textarea, DateInput
from .models import Tasks, Labels, TaskLogHours, TaskNotes
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget


class TaskCreationForm(forms.ModelForm):


    task_label = forms.CharField(required=False)
    task_due_date = forms.DateField(required=False)    
    label_list = Labels.objects.filter(label_status = 'Active')
    task_label = forms.ModelMultipleChoiceField(queryset = label_list, 
                                                widget = forms.SelectMultiple, 
                                                required = False)

    class Meta:

        model = Tasks
        fields = ('task_details','task_due_date','task_label')
        widgets = {'task_details': Textarea(attrs={'cols': 40, 'rows': 5}),
                   'task_due_date': AdminDateWidget()}


class TaskUpdationForm(forms.ModelForm):


    task_label = forms.CharField(required=False)
    task_due_date = forms.DateField(required=False)
    label_list = Labels.objects.filter(label_status = 'Active')
    task_label = forms.ModelMultipleChoiceField(queryset = label_list, 
                                                widget = forms.SelectMultiple, 
                                                required = False)

    class Meta:

        model = Tasks
        fields = ('task_details','task_due_date','task_label','task_status')
        widgets = {'task_details': Textarea(attrs={'cols': 40, 'rows': 5}),
                   'task_due_date': DateInput()}


class LabelCreationForm(forms.ModelForm):

    class Meta:
        model = Labels
        fields = ('label_name',)


class TaskLogHoursForm(forms.ModelForm):

    class Meta:

        task_log_notes = forms.CharField(required=False)
        model = TaskLogHours
        fields = ('task_time_spent','task_day_of_work', 'task_log_notes')
        widgets = {'task_log_notes': Textarea(attrs={'cols': 40, 'rows': 5}),
                   'task_time_spent': DateInput()}


class TaskNotesForm(forms.ModelForm):

    class Meta:
        task_notes = forms.CharField(required=False)
        model = TaskNotes
        fields = ('task_notes',)
        widgets = {'task_notes': Textarea(attrs={'cols': 100, 'rows': 1})}