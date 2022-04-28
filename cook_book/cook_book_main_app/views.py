from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic as views

from cook_book.cook_book_main_app.forms import CreateRecipeForm, CommentForm
from cook_book.cook_book_main_app.helper import max_files_upload_allowed
from cook_book.cook_book_main_app.models import CookedMeal, MealImage, Like


class LandingPage(views.TemplateView):
    template_name = 'landing_page.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('all recipes')
        return super().dispatch(request, *args, **kwargs)


# class DashboardView(views.TemplateView):
#     template_name = ''

class AllRecipesView(views.ListView):
    model = CookedMeal
    template_name = 'meals_view.html'


class BaseView(views.ListView):
    _TYPE = ''

    model = CookedMeal
    template_name = 'meals_view.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(type=self._TYPE)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'recipe': self._TYPE,
        })
        return context


class StartersView(BaseView):
    _TYPE = CookedMeal.STARTER


class PastaView(BaseView):
    _TYPE = CookedMeal.PASTA


class MealView(BaseView):
    _TYPE = CookedMeal.MEAL


class CakesView(BaseView):
    _TYPE = CookedMeal.CAKE


class DesertsView(BaseView):
    _TYPE = CookedMeal.SWEET


class VeganView(BaseView):
    _TYPE = CookedMeal.VEGAN


@login_required()
def create_recipe(request):
    if request.method == 'POST':
        form = CreateRecipeForm(request.POST)
        if form.is_valid():
            try:
                recipe = form.save(commit=False)
                recipe.user = request.user
                recipe.save()
                return redirect('upload files', recipe.id)
            except IntegrityError:
                error_message = render_to_string('duplicate_recipe.html', {'error': 'Рецептата се дублира'})
                response = HttpResponse(error_message)
                return response
    else:
        form = CreateRecipeForm()
    context = {
        'form': form,
    }
    return render(request, 'create_recipe.html', context)


@login_required()
def create_recipe_images(request, pk):
    recipe = CookedMeal.objects.get(pk=pk)
    current_files = recipe.mealimage_set.count()
    max_files_allowed = max_files_upload_allowed(current_files)
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        for f in files:
            image = MealImage(
                image=f,
                meal=recipe
            )
            image.save()
        return redirect('my recipes')
    context = {
        'recipe': recipe,
        'max_files_allowed': max_files_allowed,
    }
    return render(request, 'uploader.html', context)


class EditRecipeView(views.UpdateView, LoginRequiredMixin):
    model = CookedMeal
    form_class = CreateRecipeForm
    template_name = 'edit_recipe.html'

    def get_success_url(self):
        recipe_id = self.object.pk
        return reverse_lazy('my recipe details', kwargs={'pk': recipe_id})


class DeleteRecipeView(views.DeleteView, LoginRequiredMixin):
    model = CookedMeal
    template_name = 'delete_recipe.html'
    success_url = reverse_lazy('my recipes')


@login_required()
def delete_image(request, pk):
    image = MealImage.objects.get(pk=pk)
    if image:
        recipe_id = image.meal.id
        image.delete()
        return redirect('my recipe images', recipe_id)


class RecipeDetailsView(views.DetailView):
    model = CookedMeal
    template_name = 'recipe_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ingredients = self.object.ingredients.split('\r\n')
        comments = self.object.comment_set.all()
        likes_count = self.object.like_set.all().count()
        like = ''
        if self.request.user.is_authenticated:
            like = self.object.like_set.filter(user=self.request.user)

        context.update({
            'ingredients': ingredients,
            'comments': comments,
            'comment_form': CommentForm(),
            'likes_count': likes_count,
            'liked': like,
            'is_owner': self.object.user == self.request.user
        })

        return context


@login_required()
def create_comment(request, pk):
    recipe = CookedMeal.objects.get(pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.recipe = recipe
        comment.save()
    return redirect('recipe details', recipe.id)


@login_required()
def recipe_like(request, pk):
    recipe = CookedMeal.objects.get(pk=pk)
    like, created = Like.objects.get_or_create(
        user=request.user,
        recipe=recipe
    )

    if created:
        like.save()

    return redirect('recipe details', recipe.id)


class MyRecipesView(views.ListView, LoginRequiredMixin):
    model = CookedMeal
    template_name = 'my_recipes.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class MyRecipeDetailsView(RecipeDetailsView, LoginRequiredMixin):
    model = CookedMeal
    template_name = 'my_recipe_details.html'


class MyRecipePicturesView(views.DetailView, LoginRequiredMixin):
    model = CookedMeal
    template_name = 'my_recipe_images.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        max_files = 6

        context.update({
            'full': self.object.mealimage_set.count() >= max_files,
        })
        return context


@login_required()
def add_recipe_images(request, pk):
    recipe = CookedMeal.objects.get(pk=pk)
    current_files = recipe.mealimage_set.count()
    max_files_allowed = max_files_upload_allowed(current_files)
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        for f in files:
            image = MealImage(
                image=f,
                meal=recipe
            )
            image.save()
        return redirect('my recipe images', recipe.id)
    context = {
        'recipe': recipe,
        'max_files_allowed': max_files_allowed,
    }
    return render(request, 'my_images_uploader.html', context)


def internal_error(request):
    return render(request, 'errors.html')
