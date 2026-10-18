from rest_framework import serializers

from accounts.models import User
from projects.models import Project
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.IntegerField(
        source="created_by_id",
        read_only=True,
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "project",
            "assigned_to",
            "created_by",
            "status",
            "priority",
            "deadline",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_by",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        project = attrs.get(
            "project",
            getattr(self.instance, "project", None),
        )
        assignee = attrs.get(
            "assigned_to",
            getattr(self.instance, "assigned_to", None),
        )

        if assignee and project:
            if not assignee.is_active:
                raise serializers.ValidationError({
                    "assigned_to": "The selected user is inactive."
                })

            if not project.members.filter(pk=assignee.pk).exists():
                raise serializers.ValidationError({
                    "assigned_to": (
                        "The assignee must be a member of this project."
                    )
                })

        return attrs