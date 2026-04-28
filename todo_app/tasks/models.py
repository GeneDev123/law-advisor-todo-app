from django.db import models

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    position = models.FloatField(db_index=True)

    def __str__(self):
        return self.title