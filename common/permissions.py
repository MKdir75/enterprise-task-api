from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    message = "Only admins can perform this action."

    def has_permission(self, request, view):
        user = request.user

        return bool(
            user
            and user.is_authenticated
            and user.is_active
            and user.role == "ADMIN"
        )


class IsAdminOrManager(BasePermission):
    message = "Only admins or managers can perform this action."

    def has_permission(self, request, view):
        user = request.user

        return bool(
            user
            and user.is_authenticated
            and user.is_active
            and user.role in ["ADMIN", "MANAGER"]
        )


class IsAdminOrReadOnly(BasePermission):
    message = "Only admins can modify this resource."

    def has_permission(self, request, view):
        user = request.user

        if not (
            user
            and user.is_authenticated
            and user.is_active
        ):
            return False

        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        return user.role == "ADMIN"