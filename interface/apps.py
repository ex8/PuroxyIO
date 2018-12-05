from django.apps import AppConfig


class InterfaceConfig(AppConfig):
    name = 'interface'

    def ready(self):
        import interface.signals
