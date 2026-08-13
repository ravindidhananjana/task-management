from rest_framework import serializers

from .models import Project,Task


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "owner",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "owner",
            "created_at",
        ]

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "assigned_to",
            "project",
            "due_date",
            "is_deleted",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "is_deleted",
            "created_at",
            "updated_at",
        ]