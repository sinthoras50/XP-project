from django.apps import AppConfig


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

class EditorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'editor'