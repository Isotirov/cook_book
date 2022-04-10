from django.urls import path

from cook_book.cook_book_auth.views import SignIn, LogOut, SignUp, login_user

urlpatterns = [
    path('sign-up/', SignUp.as_view(), name='sign up'),
    path('sign-in/', login_user, name='sign in'),
    path('log-out/', LogOut.as_view(), name='log out'),
]
