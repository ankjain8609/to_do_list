from django.db import models
from django.contrib.auth.models import User
from datetime import date 


class Tasks(models.Model):


    user = models.ForeignKey(User, on_delete = models.CASCADE, default = 1)
    
    task_details = models.CharField('Details', max_length=500)
    task_create_time = models.DateTimeField('Task Creation Time')
    task_due_date = models.DateField('Task Due Date', null=True)
    task_last_updated_time = models.DateTimeField('Task Last Update Time')
    task_completed_time = models.DateTimeField('Task Completion Time', null=True)

    task_order_status_master = (('Open','Open'), ('Done', 'Done'),
                                ('In Progress', 'In Progress'), ('Deleted', 'Deleted'))
    task_status = models.CharField(choices= task_order_status_master, 
                                   default = 'Open', max_length=100)
    
    task_category = models.CharField('Task Category', max_length=200, null = True)
    task_label = models.CharField('Task Label', max_length=200, null = True)

    @property
    def task_is_past_due(self):
        return date.today() > self.task_due_date
    
    @property
    def task_is_completed_past_due(self):
        return self.task_completed_time.date() > self.task_due_date

    def __str__(self):
        return self.task_details


class Labels(models.Model):


    user = models.ForeignKey(User, on_delete = models.CASCADE, default = 1)
    label_name = models.CharField('Label', max_length = 100)
    label_status_master = (('Active','Active'), ('Deleted', 'Deleted'))
    label_status = models.CharField(choices= label_status_master, 
                                    default = 'Active', max_length=100)
    label_create_time = models.DateTimeField('Label Creation Time')
    label_delete_time = models.DateTimeField('Label Completion Time', null=True)

    def __str__(self):
        return self.label_name


class TaskLogHours(models.Model):


    task = models.ForeignKey(Tasks, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE, default = 1)
    task_time_spent = models.DecimalField('Task Time Spent', null = False, 
                                          max_digits=5, decimal_places=1)
    task_day_of_work = models.DateField('Task Day of Work', null= False)
    task_log_notes = models.CharField('Task Notes', max_length = 500, null = True)
    task_log_time = models.DateTimeField('Task Log Time', null = False)

    def __str__(self):
        return self.task.task_details


class TaskNotes(models.Model):


    task = models.ForeignKey(Tasks, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE, default = 1)
    task_notes = models.CharField('Task Notes', max_length = 500, null = True)
    task_note_time = models.DateTimeField('Notes Capture Time', null = False)

    def __str__(self):
        return self.task.task_details


    
