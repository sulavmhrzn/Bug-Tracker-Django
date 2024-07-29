from django.db import models
from tinymce.models import HTMLField

from accounts.models import User
from projects.models import Project


class Bug(models.Model):
    class PRIORITY(models.TextChoices):
        LOW = "L", "Low"
        MEDIUM = "M", "Medium"
        HIGH = "H", "High"

    class STATUS(models.TextChoices):
        IN_PROGRESS = "I", "In Progress"
        OPEN = "O", "Open"
        CLOSED = "C", "Closed"

    title = models.CharField(max_length=255)
    description = HTMLField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="bug")
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.CharField(
        max_length=200, choices=PRIORITY.choices, default=PRIORITY.LOW
    )
    status = models.CharField(
        max_length=200, choices=STATUS.choices, default=STATUS.IN_PROGRESS
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    description = models.TextField()
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description
