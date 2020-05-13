from django.db import models

class Tasks(models.Model):
    details = models.CharField(max_length=500)
    create_time = models.DateTimeField('Task Creation Time')
    last_updated_time = models.DateTimeField('Task Last Update Time')
    due_date = models.DateField('Task Due Date', null=True)
    completed_time = models.DateTimeField('Task Completion Time', null=True)

    ORDER_STATUS = ((0, 'Open'), (1, 'Done'), (2, 'Progress'), (3, 'Deleted'))
    status = models.SmallIntegerField(choices=ORDER_STATUS, default = 0)

    def __str__(self):
        return self.details

