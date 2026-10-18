import logging

logger = logging.getLogger(__name__)


def log_user_action(user, action, resource):
    username = getattr(user, "username", "anonymous")

    logger.info(
        "User action | username=%s | action=%s | resource=%s",
        username,
        action,
        resource,
    )


def get_client_ip(request):
    return request.META.get("REMOTE_ADDR")