from django.contrib import admin

from .models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "action",
        "model_name",
        "object_id",
        "timestamp",
    )

    list_filter = (
        "action",
        "model_name",
        "timestamp",
    )

    search_fields = (
        "user__username",
        "model_name",
        "object_id",
    )

    ordering = (
        "-timestamp",
    )

    readonly_fields = (
        "user",
        "action",
        "model_name",
        "object_id",
        "timestamp",
    )