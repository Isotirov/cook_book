from django.contrib import admin

from cook_book.cook_book_main_app.models import CookedMeal, MealImage


@admin.register(CookedMeal)
class AdminRecipes(admin.ModelAdmin):
    pass


@admin.register(MealImage)
class AdminMealImage(admin.ModelAdmin):
    pass
