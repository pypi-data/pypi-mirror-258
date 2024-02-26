"""
Конфигурация приложения email_auth_remote
"""

from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class EmailAuthRemoteConfig(AppConfig):
    """
    Приложение отвечающие за email_auth_remote
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "email_auth_remote"

    def ready(self) -> None:
        """
        После загрузки приложения импортирует spectacular схему.
        Проверяет наличие AUTH_ENDPOINT_URL.
        """
        from .extensions import (  # pylint: disable=import-outside-toplevel, unused-import
            EndpointAuthenticationExtension,
        )

        if not hasattr(settings, "AUTH_ENDPOINT_URL"):
            raise ImproperlyConfigured("AUTH_ENDPOINT_URL must be set in settings.")
