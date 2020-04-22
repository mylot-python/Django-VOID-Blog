from django.apps import AppConfig


class BangumiConfig(AppConfig):
    name = 'bangumi'

    def ready(self):
        import bangumi.signals