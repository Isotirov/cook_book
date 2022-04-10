from django.contrib.auth import get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import generic as views

from cook_book.cook_book_auth.forms import SignInForm, SignUpForm
from cook_book.cook_book_auth.helper import calculate_session_expiry_duration

UserModel = get_user_model()


class SignUp(views.CreateView):
    model = UserModel
    form_class = SignUpForm
    template_name = 'sign_up.html'
    success_url = reverse_lazy('sign in')


class SignIn(LoginView):
    authentication_form = SignInForm
    template_name = 'sign_in.html'

    def get_success_url(self):
        return reverse_lazy('landing page')


def login_user(request):
    period = calculate_session_expiry_duration()
    response = SignIn.as_view()(request)
    if 'remember' in request.POST:
        request.session.set_expiry(period)
    else:
        request.session.set_expiry(0)
    return response


class LogOut(LoginRequiredMixin, views.RedirectView):
    url = reverse_lazy('landing page')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)
