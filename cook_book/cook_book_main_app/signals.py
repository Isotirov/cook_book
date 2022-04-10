from django.db.models.signals import post_save
from django.dispatch import receiver

from cook_book.cook_book_main_app.models import CookedMeal


@receiver(post_save, sender=CookedMeal)
def check_initial_images_existence(created, instance, **kwargs):
    if created:
        if hasattr(instance, 'image_set'):
            instance.initial_images = True
