from django import forms
from django.forms import ModelForm, Textarea, DateInput
from .models import Tasks, Labels, TaskLogHours, TaskNotes
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget
from bootstrap_datepicker_plus import DatePickerInput
from datetimepicker.widgets import DateTimePicker
from django.contrib.admin import widgets


class TaskCreationForm(forms.ModelForm):
                            

    due_date = forms.DateField(required=False)    
    label_list = Labels.objects.filter(status = 'Active')
    label = forms.ModelMultipleChoiceField(queryset = label_list, 
                                           widget = forms.SelectMultiple, 
                                           required = False)

    class Meta:

        model = Tasks
        fields = ('details','due_date','label')
        widgets = {'details': Textarea(attrs={'cols': 40, 'rows': 5})}


class TaskUpdationForm(forms.ModelForm):


    due_date = forms.DateField(required=False)
    label_list = Labels.objects.filter(status = 'Active')
    label = forms.ModelMultipleChoiceField(queryset = label_list, 
                                           widget = forms.SelectMultiple, 
                                           required = False)

    class Meta:

        model = Tasks
        fields = ('details','due_date','label','status')
        widgets = {'details': Textarea(attrs={'cols': 40, 'rows': 5}),
                   'due_date': DateInput()}


class LabelCreationForm(forms.ModelForm):
    

    class Meta:
        model = Labels
        fields = ('name',)


class LabelFilterForm(forms.ModelForm):


    label_list = Labels.objects.filter(status = 'Active')
    label = forms.ModelChoiceField(queryset = label_list, 
                                      widget = forms.SelectMultiple, 
                                      required = False)

    class Meta:
        model = Labels
        fields = ('label',)


class TaskLogHoursForm(forms.ModelForm):

    class Meta:

        log_notes = forms.CharField(required=False)
        model = TaskLogHours
        fields = ('time_spent','day_of_work', 'log_notes')
        widgets = {'log_notes': Textarea(attrs={'cols': 40, 'rows': 5}),
                   'time_spent': DateInput()}


class TaskNotesForm(forms.ModelForm):

    class Meta:
        task_notes = forms.CharField(required=False)
        model = TaskNotes
        fields = ('notes',)
        widgets = {'notes': Textarea(attrs={'cols': 100, 'rows': 1})}

