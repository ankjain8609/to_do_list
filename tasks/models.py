from django.db import models

class Tasks(models.Model):

    task_details = models.CharField(max_length=500)
    task_create_time = models.DateTimeField('Task Creation Time')
    task_last_updated_time = models.DateTimeField('Task Last Update Time')
    task_due_date = models.DateField('Task Due Date', null=True)
    task_completed_time = models.DateTimeField('Task Completion Time', null=True)
    task_order_status_master = ((0, 'Open'), (1, 'Done'), (2, 'Progress'), (3, 'Deleted'))
    task_status = models.SmallIntegerField(choices= task_order_status_master, default = 0)
    task_category = models.CharField(max_length=200, null = True)
    task_label = models.CharField(max_length=200, null = True)

    def __str__(self):
        return self.task_details

