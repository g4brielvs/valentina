from django.apps import AppConfig
from django.contrib.auth.signals import user_logged_in


class AppConfig(AppConfig):
    name = 'valentina.app'
    verbose_name = 'Valentina App'

    def ready(self):
        from valentina.app.signals import save_user_ip
        user_logged_in.connect(save_user_ip)
