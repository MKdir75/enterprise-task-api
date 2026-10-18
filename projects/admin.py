from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "created_by",
        "status",
        "deadline",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
        "created_by__username",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    filter_horizontal = ("members",)

    ordering = ("-created_at",)