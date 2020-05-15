from django.db import models

class Tasks(models.Model):

    task_details = models.CharField('Details', max_length=500)
    task_create_time = models.DateTimeField('Task Creation Time')
    task_last_updated_time = models.DateTimeField('Task Last Update Time')
    task_due_date = models.DateField('Task Due Date', null=True)
    task_completed_time = models.DateTimeField('Task Completion Time', null=True)
    task_order_status_master = (('Open','Open'), ('Done', 'Done'), ('In Progress', 'In Progress'), ('Deleted', 'Deleted'))
    task_status = models.CharField(choices= task_order_status_master, default = 'Open', max_length=100)
    task_category = models.CharField('Category', max_length=200, null = True)
    task_label = models.CharField('Label', max_length=200, null = True)

    def __str__(self):
        return self.task_details
