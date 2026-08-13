from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from activity_logs.models import ActivityLog
from .models import Project, Task


class TaskManagementAPITests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username="testadmin",
            password="AdminPass123!",
        )
        self.admin.role = User.Role.ADMIN
        self.admin.save()

        self.member = User.objects.create_user(
            username="testmember",
            password="MemberPass123!",
        )
        self.member.role = User.Role.MEMBER
        self.member.save()

        self.other_member = User.objects.create_user(
            username="othermember",
            password="OtherPass123!",
        )
        self.other_member.role = User.Role.MEMBER
        self.other_member.save()

        self.project = Project.objects.create(
            name="Test Project",
            description="Project for automated testing.",
            owner=self.admin,
        )

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def create_task(self, assigned_to=None, title="Test Task"):
        return Task.objects.create(
            title=title,
            description="Task created during testing.",
            status="TODO",
            priority="MEDIUM",
            assigned_to=assigned_to,
            project=self.project,
            due_date="2026-09-01",
        )

    # 1. LOGIN TEST
    def test_login(self):
        url = reverse("token_obtain_pair")

        response = self.client.post(
            url,
            {
                "username": "testadmin",
                "password": "AdminPass123!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    # 2. TASK CREATION TEST
    def test_member_can_create_task(self):
        self.authenticate(self.member)

        url = reverse("task-list")

        response = self.client.post(
            url,
            {
                "title": "Member Created Task",
                "description": "Testing member task creation.",
                "status": "TODO",
                "priority": "LOW",
                "project": self.project.id,
                "due_date": "2026-09-02",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        task = Task.objects.get(id=response.data["id"])

        self.assertEqual(task.assigned_to, self.member)
        self.assertFalse(task.is_deleted)

    # 3. PERMISSION TEST
    def test_member_cannot_update_unassigned_task(self):
        task = self.create_task(
            assigned_to=self.other_member,
            title="Protected Task",
        )

        self.authenticate(self.member)

        url = reverse(
            "task-detail",
            kwargs={"pk": task.id},
        )

        response = self.client.patch(
            url,
            {"title": "Unauthorized Update"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        task.refresh_from_db()

        self.assertEqual(
            task.title,
            "Protected Task",
        )

    # 4. SOFT DELETE TEST
    def test_task_delete_is_soft_delete(self):
        task = self.create_task(
            assigned_to=self.member,
            title="Task To Delete",
        )

        self.authenticate(self.admin)

        url = reverse(
            "task-detail",
            kwargs={"pk": task.id},
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        task.refresh_from_db()

        self.assertTrue(task.is_deleted)

        # Deleted task must no longer appear in the API queryset.
        response = self.client.get(
            reverse("task-list")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        returned_ids = [
            item["id"]
            for item in response.data["results"]
        ]

        self.assertNotIn(task.id, returned_ids)

    # 5. ACTIVITY LOG TEST
    def test_activity_log_created_for_task_creation(self):
        self.authenticate(self.member)

        url = reverse("task-list")

        response = self.client.post(
            url,
            {
                "title": "Activity Log Test",
                "description": "Testing automatic activity logging.",
                "status": "TODO",
                "priority": "LOW",
                "project": self.project.id,
                "due_date": "2026-09-03",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        task_id = response.data["id"]

        log = ActivityLog.objects.get(
            model_name="Task",
            object_id=task_id,
            action=ActivityLog.Action.CREATE,
        )

        self.assertEqual(log.user, self.member)

    # BONUS: UPDATE ACTIVITY LOG
    def test_activity_log_created_for_task_update(self):
        task = self.create_task(
            assigned_to=self.member,
            title="Update Log Test",
        )

        # Remove the CREATE log generated by direct model creation.
        ActivityLog.objects.filter(
            model_name="Task",
            object_id=task.id,
        ).delete()

        self.authenticate(self.member)

        url = reverse(
            "task-detail",
            kwargs={"pk": task.id},
        )

        response = self.client.patch(
            url,
            {
                "title": "Updated Task",
                "status": "IN_PROGRESS",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        log = ActivityLog.objects.get(
            model_name="Task",
            object_id=task.id,
            action=ActivityLog.Action.UPDATE,
        )

        self.assertEqual(log.user, self.member)

    # BONUS: DELETE ACTIVITY LOG
    def test_activity_log_created_for_task_delete(self):
        task = self.create_task(
            assigned_to=self.member,
            title="Delete Log Test",
        )

        ActivityLog.objects.filter(
            model_name="Task",
            object_id=task.id,
        ).delete()

        self.authenticate(self.admin)

        url = reverse(
            "task-detail",
            kwargs={"pk": task.id},
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        log = ActivityLog.objects.get(
            model_name="Task",
            object_id=task.id,
            action=ActivityLog.Action.DELETE,
        )

        self.assertEqual(log.user, self.admin)