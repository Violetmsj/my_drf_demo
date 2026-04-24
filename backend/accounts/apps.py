from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = "accounts"
    verbose_name = "用户认证"

    def ready(self):
        from . import signals  # noqa: F401

