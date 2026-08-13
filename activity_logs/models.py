from django.conf import settings
from django.db import models


class ActivityLog(models.Model):
    class Action(models.TextChoices):
        CREATE = "CREATE", "Create"
        UPDATE = "UPDATE", "Update"
        DELETE = "DELETE", "Delete"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activity_logs",
    )

    action = models.CharField(
        max_length=10,
        choices=Action.choices,
    )

    model_name = models.CharField(max_length=100)

    object_id = models.PositiveBigIntegerField()

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} {self.model_name} #{self.object_id}"