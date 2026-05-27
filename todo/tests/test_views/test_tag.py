from django.test import TestCase
from django.urls import reverse

from todo.models import Tag


class TagListViewTest(TestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(name="Work")
        self.tag2 = Tag.objects.create(name="Personal")
        self.response = self.client.get(reverse("todo:tag-list"))

    def test_tag_list_view_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_tag_list_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, "todo/tag_list.html")

    def test_tag_list_view_context_contains_tags(self):
        tags = self.response.context["tags"]
        self.assertIn(self.tag1, tags)
        self.assertIn(self.tag2, tags)


class TagCreateViewTest(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse("todo:tag-create"))

    def test_get_tag_create_view_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_get_tag_create_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, "todo/tag_form.html")

    def test_post_valid_data_creates_tag_and_redirects(self):
        response = self.client.post(
            reverse("todo:tag-create"),
            {"name": "Work"}
        )
        self.assertEqual(Tag.objects.count(), 1)
        self.assertRedirects(response, reverse("todo:tag-list"))

    def test_post_invalid_data_shows_form_errors(self):
        response = self.client.post(reverse("todo:tag-create"), {"name": ""})
        self.assertEqual(Tag.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")


class TagUpdateViewTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="Work")
        self.response = self.client.get(
            reverse("todo:tag-update", args=[self.tag.pk]))

    def test_get_tag_update_view_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_get_tag_update_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, "todo/tag_form.html")

    def test_post_valid_data_updates_tag_and_redirects(self):
        response = self.client.post(
            reverse("todo:tag-update", args=[self.tag.pk]),
            {"name": "Updated Work"}
        )
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.name, "Updated Work")
        self.assertRedirects(response, reverse("todo:tag-list"))

    def test_post_invalid_data_shows_form_errors(self):
        response = self.client.post(
            reverse("todo:tag-update", args=[self.tag.pk]),
            {"name": ""}
        )
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.name, "Work")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")


class TagDeleteViewTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="Work")
        self.response_get = self.client.get(
            reverse("todo:tag-delete", args=[self.tag.pk]))
        self.response_post = self.client.post(
            reverse("todo:tag-delete", args=[self.tag.pk]))

    def test_get_tag_delete_view_status_code(self):
        self.assertEqual(self.response_get.status_code, 200)

    def test_get_tag_delete_view_uses_correct_template(self):
        self.assertTemplateUsed(
            self.response_get, "todo/todo_confirm_delete.html")

    def test_get_tag_delete_view_context_contains_delete_type(self):
        self.assertEqual(self.response_get.context["delete_type"], "tag")

    def test_post_valid_deletes_tag_and_redirects(self):
        self.assertEqual(Tag.objects.count(), 0)
        self.assertRedirects(self.response_post, reverse("todo:tag-list"))
