from django.urls import path

from cook_book.cook_book_profiles.views import ProfileView, UpdateProfileView

urlpatterns = [
    path('<int:pk>/', ProfileView.as_view(), name='profile details'),
    path('update-profile/<int:pk>/', UpdateProfileView.as_view(), name='update profile'),
]
