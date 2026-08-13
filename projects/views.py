from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from core.permissions import IsAdminOrTaskMember,IsAdminOrReadOnly
from .models import Project,Task
from .serializers import ProjectSerializer,TaskSerializer
from core.activity_context import set_current_user, reset_current_user

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        token = set_current_user(self.request.user)

        try:
            serializer.save(owner=self.request.user)
        finally:
            reset_current_user(token)

    def perform_update(self, serializer):
        token = set_current_user(self.request.user)

        try:
            serializer.save()
        finally:
            reset_current_user(token)

    def perform_destroy(self, instance):
        token = set_current_user(self.request.user)

        try:
            instance.delete()
        finally:
            reset_current_user(token)

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.filter(is_deleted=False)
    serializer_class = TaskSerializer
    permission_classes = [IsAdminOrTaskMember]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "status",
        "priority",
        "assigned_to",
        "project",
    ]

    search_fields = [
        "title",
        "description",
    ]

    ordering_fields = [
        "created_at",
        "updated_at",
        "due_date",
        "priority",
        "status",
        "title",
    ]

    ordering = ["-created_at"]

    def perform_create(self, serializer):
        token = set_current_user(self.request.user)

        try:
            if self.request.user.role == "ADMIN":
                serializer.save()
            else:
                serializer.save(assigned_to=self.request.user)
        finally:
            reset_current_user(token)


    def perform_update(self, serializer):
        token = set_current_user(self.request.user)

        try:
            serializer.save()
        finally:
            reset_current_user(token)


    def perform_destroy(self, instance):
        token = set_current_user(self.request.user)

        try:
            instance._activity_delete = True
            instance.is_deleted = True
            instance.save(update_fields=["is_deleted"])
        finally:
            reset_current_user(token)