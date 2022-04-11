from django.urls import path

from cook_book.cook_book_auth.views import LogOut, login_user, activate, SignUp

urlpatterns = [
    path('sign-up/', SignUp.as_view(), name='sign up'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
    path('sign-in/', login_user, name='sign in'),
    path('log-out/', LogOut.as_view(), name='log out'),
]
