from rest_framework import serializers
from .models import ActivityLog


class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = [
            "id",
            "user",
            "action",
            "model_name",
            "object_id",
            "timestamp",
        ]
        read_only_fields = fields