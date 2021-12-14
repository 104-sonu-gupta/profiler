from django.apps import AppConfig
from django.db.models import signals


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # initially app dont know about signal so we need to update the app for signals

    def ready(self) -> None:
        import users.signals


