from django.db import models
from django.contrib.auth.models import User
from datetime import date 


class Tasks(models.Model):


    user = models.ForeignKey(User, on_delete = models.CASCADE, default = 1)
    
    details = models.CharField('Details', max_length=500)
    create_time = models.DateTimeField('Task Creation Time')
    due_date = models.DateField('Task Due Date', null=True)
    last_updated_time = models.DateTimeField('Task Last Update Time')
    completed_time = models.DateTimeField('Task Completion Time', null=True)

    order_status_master = (('Open','Open'), ('Done', 'Done'),
                          ('In Progress', 'In Progress'), ('Deleted', 'Deleted'))
    status = models.CharField(choices= order_status_master, 
                              default = 'Open', max_length=100)
    
    category = models.CharField('Task Category', max_length=200, null = True)
    label = models.CharField('Task Label', max_length=200, null = True)

    @property
    def task_is_past_due(self):
        return date.today() > self.due_date
    
    @property
    def task_is_completed_past_due(self):
        return self.completed_time.date() > self.due_date

    def __str__(self):
        return self.details


class Labels(models.Model):


    user = models.ForeignKey(User, on_delete = models.CASCADE, default = 1)
    name = models.CharField('Label Name', max_length = 100)
    
    status_master = (('Active','Active'), ('Deleted', 'Deleted'))
    status = models.CharField(choices= status_master, 
                                    default = 'Active', max_length=100)
    
    create_time = models.DateTimeField('Label Creation Time')
    delete_time = models.DateTimeField('Label Completion Time', null=True)

    def __str__(self):
        return self.name


class TaskLogHours(models.Model):


    task = models.ForeignKey(Tasks, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE, default = 1)
    time_spent = models.DecimalField('Task Time Spent', null = False, 
                                      max_digits=5, decimal_places=2)
    day_of_work = models.DateField('Task Day of Work', null= False)
    log_notes = models.CharField('Task Notes', max_length = 500, null = True)
    log_time = models.DateTimeField('Task Log Time', null = False)

    def __str__(self):
        return self.task.details


class TaskNotes(models.Model):


    task = models.ForeignKey(Tasks, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE, default = 1)
    notes = models.CharField('Task Notes', max_length = 500, null = True)
    note_time = models.DateTimeField('Notes Capture Time', null = False)

    def __str__(self):
        return self.task.details


    
