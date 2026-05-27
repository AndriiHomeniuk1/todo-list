from django.test import TestCase
from django.urls import reverse

from todo.models import Task, Tag


class IndexViewTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="Work")
        self.task = Task.objects.create(content="Buy milk")
        self.task.tags.add(self.tag)
        self.response = self.client.get(reverse("todo:index"))

    def test_index_view_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_index_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, "todo/index.html")

    def test_index_view_context_contains_tasks(self):
        tasks = self.response.context["tasks"]
        self.assertIn(self.task, tasks)
