from rest_framework.routers import DefaultRouter
from activity_logs.views import ActivityLogViewSet
from .views import ProjectViewSet,TaskViewSet


router = DefaultRouter()
router.register("projects", ProjectViewSet, basename="project")
router.register("tasks", TaskViewSet, basename="task")
router.register(r"activity-logs", ActivityLogViewSet, basename="activity-log")
urlpatterns = router.urls