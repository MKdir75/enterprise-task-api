from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
from .models import Project
from .serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == User.Role.ADMIN:
            return Project.objects.all().prefetch_related("members")

        if user.role == User.Role.MANAGER:
            return Project.objects.filter(
                created_by=user
            ).prefetch_related("members")

        return Project.objects.filter(
            members=user
        ).prefetch_related("members")

    def perform_create(self, serializer):
        user = self.request.user

        if user.role not in [User.Role.ADMIN, User.Role.MANAGER]:
            raise PermissionDenied(
                "Only admins and managers can create projects."
            )

        serializer.save(created_by=user)

    def perform_update(self, serializer):
        user = self.request.user
        project = self.get_object()

        if user.role != User.Role.ADMIN and project.created_by_id != user.id:
            raise PermissionDenied(
                "You cannot update this project."
            )

        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user

        if user.role != User.Role.ADMIN and instance.created_by_id != user.id:
            raise PermissionDenied(
                "You cannot delete this project."
            )

        instance.delete()