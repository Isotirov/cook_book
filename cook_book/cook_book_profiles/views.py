from babel.dates import format_date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic as views

from cook_book.cook_book_main_app.models import CookedMeal, Like
from cook_book.cook_book_profiles.forms import UpdateProfileForm
from cook_book.cook_book_profiles.models import CookBookUserProfile


class UpdateProfileView(views.UpdateView, LoginRequiredMixin):
    model = CookBookUserProfile
    template_name = 'update_profile.html'
    form_class = UpdateProfileForm

    def get_success_url(self):
        profile_id = self.object.pk
        return reverse_lazy('profile details', kwargs={'pk': profile_id})


class ProfileView(views.DetailView, LoginRequiredMixin):
    model = CookBookUserProfile
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipes = CookedMeal.objects.filter(user=self.request.user)
        recipes_likes_count = Like.objects.filter(recipe__in=recipes).count()
        date = self.object.joined

        context.update({
            'recipes_count': recipes.count(),
            'recipes_likes_count': recipes_likes_count,
            'date': format_date(date, format='long', locale='bg')
        })

        return context
