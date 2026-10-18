from django.db.models import Q
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    filterset_fields = ["status", "priority", "project", "assigned_to"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "deadline", "priority"]

    def get_queryset(self):
        user = self.request.user

        queryset = Task.objects.select_related(
            "project", "assigned_to", "created_by"
        )

        if user.role == User.Role.ADMIN:
            return queryset

        if user.role == User.Role.MANAGER:
            return queryset.filter(project__created_by=user)

        return queryset.filter(
            Q(project__members=user) &
            (Q(assigned_to=user) | Q(status__in=["TODO", "IN_PROGRESS", "REVIEW", "COMPLETED", "CANCELLED"]))
        ).distinct()

    def perform_create(self, serializer):
        user = self.request.user

        if user.role not in [User.Role.ADMIN, User.Role.MANAGER]:
            raise PermissionDenied(
                "Only admins and managers can create tasks."
            )

        project = serializer.validated_data["project"]

        if user.role != User.Role.ADMIN:
            if project.created_by_id != user.id:
                raise PermissionDenied(
                    "You can create tasks only in your own projects."
                )

        serializer.save(created_by=user)

    def perform_update(self, serializer):
        user = self.request.user
        task = self.get_object()

        if user.role == User.Role.ADMIN:
            serializer.save()
            return

        if user.role == User.Role.MANAGER:
            if task.project.created_by_id != user.id:
                raise PermissionDenied("You cannot update this task.")
            serializer.save()
            return

        if user.role == User.Role.DEVELOPER:
            if task.assigned_to_id != user.id:
                raise PermissionDenied(
                    "You can update only tasks assigned to you."
                )

            allowed_fields = {"status"}
            changed_fields = set(serializer.validated_data.keys())

            if not changed_fields.issubset(allowed_fields):
                raise PermissionDenied(
                    "Developers can update only task status."
                )

            serializer.save()
            return

        raise PermissionDenied("You cannot update this task.")

    def perform_destroy(self, instance):
        user = self.request.user

        if user.role == User.Role.ADMIN:
            instance.delete()
            return

        if (
            user.role == User.Role.MANAGER
            and instance.project.created_by_id == user.id
        ):
            instance.delete()
            return

        raise PermissionDenied("You cannot delete this task.")