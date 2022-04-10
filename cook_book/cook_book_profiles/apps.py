from django.apps import AppConfig


class CookBookProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cook_book.cook_book_profiles'

    def ready(self):
        import cook_book.cook_book_profiles.signals
