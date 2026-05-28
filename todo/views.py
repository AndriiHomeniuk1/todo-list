from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic.detail import SingleObjectMixin

from todo.forms import TaskForm
from todo.models import Tag, Task


def index(request: HttpRequest) -> HttpResponse:
    tasks = Task.objects.prefetch_related("tags")

    context = {
        "tasks": tasks
    }

    return render(request, "todo/index.html", context)


class TagListView(generic.ListView):
    model = Tag
    template_name = "todo/tag_list.html"
    context_object_name = "tags"


class TagCreateView(generic.CreateView):
    model = Tag
    fields = ["name"]
    template_name = "todo/tag_form.html"
    success_url = reverse_lazy("todo:tag-list")


class TagUpdateView(generic.UpdateView):
    model = Tag
    fields = ["name"]
    template_name = "todo/tag_form.html"
    success_url = reverse_lazy("todo:tag-list")


class TagDeleteView(generic.DeleteView):
    model = Tag
    template_name = "todo/todo_confirm_delete.html"
    success_url = reverse_lazy("todo:tag-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"delete_type": "tag"})
        return context


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = "todo/task_form.html"
    success_url = reverse_lazy("todo:index")


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "todo/task_form.html"
    success_url = reverse_lazy("todo:index")


class TaskDeleteView(generic.DeleteView):
    model = Task
    template_name = "todo/todo_confirm_delete.html"
    success_url = reverse_lazy("todo:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"delete_type": "task"})
        return context


class ToggleTaskView(SingleObjectMixin, View):
    model = Task

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.is_completed = not task.is_completed
        task.save()
        return redirect("todo:index")
