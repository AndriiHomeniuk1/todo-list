from django.test import TestCase
from todo.forms import TaskForm
from django.forms.widgets import CheckboxSelectMultiple

from todo.models import Tag


class TaskFormTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="Work")

    def test_form_has_correct_fields(self):
        form = TaskForm()
        self.assertIn("content", form.fields)
        self.assertIn("deadline", form.fields)
        self.assertIn("tags", form.fields)

    def test_deadline_widget_is_datetime_local(self):
        form = TaskForm()
        deadline_widget = form.fields["deadline"].widget
        self.assertEqual(deadline_widget.input_type, "datetime-local")
        self.assertIn("form-control", deadline_widget.attrs.get("class", ""))


    def test_tags_widget_is_checkbox_multiple(self):
        form = TaskForm()
        tags_widget = form.fields["tags"].widget
        self.assertIsInstance(tags_widget, CheckboxSelectMultiple)
        self.assertIn("form-check", tags_widget.attrs.get("class", ""))


    def test_form_valid_data_creates_task(self):
        form = TaskForm(data={
            "content": "Buy milk",
            "deadline": "2026-05-27T19:00",
            "tags": [self.tag.pk],
        })
        self.assertTrue(form.is_valid())
        task = form.save()
        self.assertEqual(task.content, "Buy milk")
        self.assertIn(self.tag, task.tags.all())

    def test_form_invalid_without_content(self):
        form = TaskForm(data={
            "content": "",
            "deadline": "2026-05-27T19:00",
            "tags": [self.tag.pk],
        })
        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)
