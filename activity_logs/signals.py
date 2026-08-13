from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from activity_logs.models import ActivityLog
from core.activity_context import get_current_user
from projects.models import Project, Task


@receiver(post_save, sender=Project)
def log_project_save(sender, instance, created, **kwargs):
    action = (
        ActivityLog.Action.CREATE
        if created
        else ActivityLog.Action.UPDATE
    )

    ActivityLog.objects.create(
        user=get_current_user(),
        action=action,
        model_name="Project",
        object_id=instance.pk,
    )


@receiver(post_delete, sender=Project)
def log_project_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        user=get_current_user(),
        action=ActivityLog.Action.DELETE,
        model_name="Project",
        object_id=instance.pk,
    )


@receiver(post_save, sender=Task)
def log_task_save(sender, instance, created, **kwargs):
    if getattr(instance, "_activity_delete", False):
        action = ActivityLog.Action.DELETE
    elif created:
        action = ActivityLog.Action.CREATE
    else:
        action = ActivityLog.Action.UPDATE

    ActivityLog.objects.create(
        user=get_current_user(),
        action=action,
        model_name="Task",
        object_id=instance.pk,
    )