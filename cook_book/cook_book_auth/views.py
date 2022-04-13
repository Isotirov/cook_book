from django.contrib.auth import get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import generic as views
from django.contrib.auth import views as pass_views

from cook_book.cook_book_auth.forms import SignInForm, SignUpForm
from cook_book.cook_book_auth.helper import calculate_session_expiry_duration
from cook_book.cook_book_auth.tokens import account_activation_token, TokenGenerator

UserModel = get_user_model()


class SignUp(views.CreateView):
    model = UserModel
    form_class = SignUpForm
    template_name = 'sign_up.html'
    success_url = reverse_lazy('sign in')

    def send_activation_email(self, request, user):
        current_site = get_current_site(self.request)
        mail_subject = 'Добре дошли в домашния кулинарник.'
        message = render_to_string('acc_active_email.html', {
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = user.email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            self.send_activation_email(self, user)
            return redirect('mail sent')
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        if UserModel.objects.filter(email=request.POST['email']).exists():
            user = UserModel.objects.get(email=request.POST['email'])
            if not user.is_active:
                self.send_activation_email(request, user)
                return redirect('mail sent')
        return super().post(request, *args, **kwargs)


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('success activation')
    else:
        return HttpResponse('Линка е невалиден!')


def remember_me(request):
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


class ShowTemplateEmailSend(views.TemplateView):
    template_name = 'mail_sent.html'


class ShowTemplateActivationSuccess(views.TemplateView):
    template_name = 'success_activation.html'


class PasswordChangeViewCustom(pass_views.PasswordChangeView):
    pass


class PasswordResetViewCustom(pass_views.PasswordResetView):
    template_name = 'reset_password.html'
    email_template_name = 'password_reset_email.html'
    title = 'Смяна на парола'
    success_url = reverse_lazy('reset password sent')

    def form_valid(self, form):
        if not UserModel.objects.filter(email=self.request.POST['email']).exists():
            return redirect('not registered')
        return super().form_valid(form)


class ResetPasswordSent(views.TemplateView):
    template_name = 'reset_mail_sent.html'


class NoSuchEmail(views.TemplateView):
    template_name = 'user_does_not_exists.html'
