from django.test import TestCase
from django.urls import reverse

from todo.models import Task


class TaskCreateViewTest(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse("todo:task-create"))

    def test_get_task_create_view_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_get_task_create_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, "todo/task_form.html")

    def test_post_valid_data_creates_task_and_redirects(self):
        response = self.client.post(
            reverse("todo:task-create"),
            {"content": "Buy milk"}
        )
        self.assertEqual(Task.objects.count(), 1)
        self.assertRedirects(response, reverse("todo:index"))

    def test_post_invalid_data_shows_form_errors(self):
        response = self.client.post(
            reverse("todo:task-create"), {"content": ""})
        self.assertEqual(Task.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")


class TaskUpdateViewTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(content="Buy milk")
        self.response_get = self.client.get(
            reverse("todo:task-update", args=[self.task.pk]))

    def test_get_task_update_view_status_code(self):
        self.assertEqual(self.response_get.status_code, 200)

    def test_get_task_update_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response_get, "todo/task_form.html")

    def test_post_valid_data_updates_task_and_redirects(self):
        response = self.client.post(
            reverse("todo:task-update", args=[self.task.pk]),
            {"content": "Buy bread"}
        )
        self.task.refresh_from_db()
        self.assertEqual(self.task.content, "Buy bread")
        self.assertRedirects(response, reverse("todo:index"))

    def test_post_invalid_data_shows_form_errors(self):
        response = self.client.post(
            reverse("todo:task-update", args=[self.task.pk]),
            {"content": ""}
        )
        self.task.refresh_from_db()
        self.assertEqual(self.task.content, "Buy milk")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")


class TaskDeleteViewTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(content="Buy milk")
        self.response_get = self.client.get(
            reverse("todo:task-delete", args=[self.task.pk]))

    def test_get_task_delete_view_status_code(self):
        self.assertEqual(self.response_get.status_code, 200)

    def test_get_task_delete_view_uses_correct_template(self):
        self.assertTemplateUsed(
            self.response_get, "todo/todo_confirm_delete.html")

    def test_get_task_delete_view_context_contains_delete_type(self):
        self.assertEqual(
            self.response_get.context["delete_type"], "task")

    def test_post_valid_deletes_task_and_redirects(self):
        response = self.client.post(
            reverse("todo:task-delete", args=[self.task.pk]))
        self.assertEqual(Task.objects.count(), 0)
        self.assertRedirects(response, reverse("todo:index"))


class ToggleTaskViewTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(content="Buy milk", is_completed=False)

    def test_post_toggles_task_completion_and_redirects(self):
        response = self.client.post(
            reverse("todo:toggle-task", args=[self.task.pk]))
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_completed)
        self.assertRedirects(response, reverse("todo:index"))

    def test_post_toggles_back_to_incomplete(self):
        self.task.is_completed = True
        self.task.save()

        response = self.client.post(
            reverse("todo:toggle-task", args=[self.task.pk]))
        self.task.refresh_from_db()
        self.assertFalse(self.task.is_completed)
        self.assertRedirects(response, reverse("todo:index"))
