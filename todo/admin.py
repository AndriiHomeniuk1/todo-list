from django.contrib import admin
from django.contrib.auth.models import Group, User

from todo.models import Tag, Task


admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(Tag)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "content",
        "datetime",
        "deadline",
        "is_completed",
    ]
    list_filter = [
        "datetime",
        "deadline",
        "is_completed",
        "tags"
    ]
    search_fields = [
        "content",
    ]
    list_editable = [
        "is_completed",
    ]
