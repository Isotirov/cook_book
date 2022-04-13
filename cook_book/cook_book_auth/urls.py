from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path

from cook_book.cook_book_auth.views import LogOut, remember_me, activate, SignUp, ShowTemplateEmailSend, \
    ShowTemplateActivationSuccess, PasswordResetViewCustom, PasswordChangeViewCustom, ResetPasswordSent, NoSuchEmail

urlpatterns = [
    path('sign-up/', SignUp.as_view(), name='sign up'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
    path('sign-in/', remember_me, name='sign in'),
    path('log-out/', LogOut.as_view(), name='log out'),

    path('mail-sent/', ShowTemplateEmailSend.as_view(), name='mail sent'),
    path('success-mail/', ShowTemplateActivationSuccess.as_view(), name='success activation'),

    path('change-password/', PasswordChangeViewCustom.as_view(), name='password change'),
    path('password-reset/', PasswordResetViewCustom.as_view(), name='password reset mail'),
    path('reset-password-sent/', ResetPasswordSent.as_view(), name='reset password sent'),
    path('invalid-email/', NoSuchEmail.as_view(), name='not registered'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='reset_password.html'), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name='success_activation.html'), name='password_reset_complete'),
]



