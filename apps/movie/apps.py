from django.apps import AppConfig


class MovieConfig(AppConfig):
    name = 'movie'

    def ready(self):
        import movie.signals
