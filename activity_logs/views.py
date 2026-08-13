from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import ActivityLog
from .serializers import ActivityLogSerializer


class ActivityLogViewSet(ReadOnlyModelViewSet):
    queryset = ActivityLog.objects.select_related("user").all()
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.role == "ADMIN":
            return queryset

        return queryset.filter(user=self.request.user)