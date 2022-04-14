from django.contrib import admin

from cook_book.cook_book_main_app.models import CookedMeal


@admin.register(CookedMeal)
class AdminRecipes(admin.ModelAdmin):
    pass
