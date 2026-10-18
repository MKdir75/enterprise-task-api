
from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "project",
        "assigned_to",
        "created_by",
        "status",
        "priority",
        "deadline",
        "created_at",
    )

    list_filter = (
        "status",
        "priority",
        "deadline",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "project__name",
        "assigned_to__username",
        "created_by__username",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_select_related = (
        "project",
        "assigned_to",
        "created_by",
    )

    ordering = ("-created_at",)

    date_hierarchy = "created_at"

