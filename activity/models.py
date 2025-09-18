from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'user')  # Prevent duplicate category names per user

    def __str__(self):
        return self.name

class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    date = models.DateField(default=date.today)

    def duration(self):
        return self.end_time - self.start_time

    def __str__(self):
        return f"{self.description} ({self.duration()})"