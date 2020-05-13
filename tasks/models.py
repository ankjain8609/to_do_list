from django.db import models

class Tasks(models.Model):
    details = models.CharField(max_length=500)
    created_at = models.DateTimeField('Task Creation Time')
    updated_at = models.DateTimeField('Task Last Update Time')
    due_date = models.DateField('Task Due Date', blank=True)
    completed_at = models.DateTimeField('Task Completion Time', blank=True)
