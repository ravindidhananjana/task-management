from rest_framework.permissions import BasePermission


class IsAdminOrTaskMember(BasePermission):
    """
    Admin users have full access.

    Members:
    - Can create tasks.
    - Can update tasks assigned to themselves.
    - Cannot delete tasks.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == "ADMIN":
            return True

        if request.method == "POST":
            return True

        if request.method == "DELETE":
            return False

        return True

    def has_object_permission(self, request, view, obj):
        if request.user.role == "ADMIN":
            return True

        if request.method in ["PUT", "PATCH"]:
            return obj.assigned_to == request.user

        if request.method == "DELETE":
            return False

        return True

class IsAdminOrReadOnly(BasePermission):
    """
    Admin users have full access.
    Members have read-only access.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == "ADMIN":
            return True

        return request.method in ["GET", "HEAD", "OPTIONS"]