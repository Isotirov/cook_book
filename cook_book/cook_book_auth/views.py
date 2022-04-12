from django.contrib.auth import get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import generic as views

from cook_book.cook_book_auth.forms import SignInForm, SignUpForm
from cook_book.cook_book_auth.helper import calculate_session_expiry_duration
from cook_book.cook_book_auth.tokens import account_activation_token

UserModel = get_user_model()


class SignUp(views.CreateView):
    model = UserModel
    form_class = SignUpForm
    template_name = 'sign_up.html'
    success_url = reverse_lazy('sign in')

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            current_site = get_current_site(self.request)
            mail_subject = 'Добре дошли в домашния кулинарник.'
            message = render_to_string('acc_active_email.html', {
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Изпратихме линк на пощата ви за потвърждение.')
        return super().form_valid(form)


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login_user(request)
        return redirect('sign in')
    else:
        return HttpResponse('Линка е невалиден!')


def login_user(request):
    period = calculate_session_expiry_duration()
    response = SignIn.as_view()(request)
    if 'remember' in request.POST:
        request.session.set_expiry(period)
    else:
        request.session.set_expiry(0)
    return response


class SignIn(LoginView):
    authentication_form = SignInForm
    template_name = 'sign_in.html'

    def get_success_url(self):
        return reverse_lazy('landing page')


class LogOut(LoginRequiredMixin, views.RedirectView):
    url = reverse_lazy('landing page')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)
