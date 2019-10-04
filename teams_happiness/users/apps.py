from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "teams_happiness.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import teams_happiness.users.signals  # noqa F401
        except ImportError:
            pass
