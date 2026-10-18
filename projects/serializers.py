from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    created_by = serializers.IntegerField(
        source="created_by_id",
        read_only=True,
    )

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "created_by",
            "members",
            "status",
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

    def validate_members(self, members):
        for member in members:
            if not member.is_active:
                raise serializers.ValidationError(
                    "Inactive users cannot be project members."
                )
        return members