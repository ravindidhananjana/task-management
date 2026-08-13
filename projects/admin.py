from django.contrib import admin

from .models import Project, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "owner",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
        "owner__username",
    )

    list_filter = (
        "created_at",
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "status",
        "priority",
        "assigned_to",
        "project",
        "due_date",
        "is_deleted",
    )

    search_fields = (
        "title",
        "description",
    )

    list_filter = (
        "status",
        "priority",
        "is_deleted",
    )

    ordering = (
        "-created_at",
    )