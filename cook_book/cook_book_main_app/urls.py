from django.urls import path

from cook_book.cook_book_main_app.views import CakesView, LandingPage, create_recipe, create_recipe_images, \
    RecipeDetailsView, AllRecipesView, PastaView, MealView, DesertsView, StartersView, VeganView, create_comment, \
    recipe_like, MyRecipesView, EditRecipeView, DeleteRecipeView, MyRecipeDetailsView, MyRecipePicturesView, \
    delete_image, add_recipe_images

urlpatterns = [
    path('', LandingPage.as_view(), name='landing page'),
    # path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('all-meals/', AllRecipesView.as_view(), name='all recipes'),
    path('starters/', StartersView.as_view(), name='starters'),
    path('pasta/', PastaView.as_view(), name='pasta'),
    path('meal/', MealView.as_view(), name='meal'),
    path('cakes/', CakesView.as_view(), name='cakes'),
    path('deserts/', DesertsView.as_view(), name='deserts'),
    path('vegan/', VeganView.as_view(), name='vegan'),

    path('create-recipe/', create_recipe, name='add recipe'),
    path('update-recipe/<int:pk>', EditRecipeView.as_view(), name='update recipe'),
    path('delete/<int:pk>/', DeleteRecipeView.as_view(), name='delete recipe'),
    path('delete-image/<int:pk>/', delete_image, name='delete image'),
    path('upload-files/<int:pk>/', create_recipe_images, name='upload files'),
    path('upload-my-files/<int:pk>/', add_recipe_images, name='upload my files'),

    path('recipe-details/<int:pk>/', RecipeDetailsView.as_view(), name='recipe details'),
    path('my-recipe-details/<int:pk>/', MyRecipeDetailsView.as_view(), name='my recipe details'),
    path('my-recipe-images/<int:pk>', MyRecipePicturesView.as_view(), name='my recipe images'),
    path('comment/<int:pk>', create_comment, name='comment'),
    path('like/<int:pk>', recipe_like, name='like'),

    path('my-recipes/', MyRecipesView.as_view(), name='my recipes'),
    # path('edit-meal/<int:pk>/', EditMealView.as_view(), name='edit meal'),
    # path('delete-meal/<int:pk>/', delete_meal, name='delete meal'),
]
