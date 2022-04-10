from django.apps import AppConfig


class CookBookMainAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cook_book.cook_book_main_app'

    def ready(self):
        import cook_book.cook_book_main_app.signals
