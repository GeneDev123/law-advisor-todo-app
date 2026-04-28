from django.db import models

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    position = models.PositiveIntegerField()

    def __str__(self):
        return self.title