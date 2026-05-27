from django.test import TestCase

from todo.models import Tag, Task


class TagModelTest(TestCase):
    def test_str_returns_name(self):
        tag = Tag.objects.create(name="Work")
        self.assertEqual(str(tag), "Work")

class TaskModelTest(TestCase):
    def test_str_returns_content(self):
        task = Task.objects.create(content="Buy milk")
        self.assertEqual(str(task), "Buy milk")
