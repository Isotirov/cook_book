from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm, SetPasswordForm
from django.core.exceptions import ValidationError

UserModel = get_user_model()


class AuthBotCatcherMixin(forms.Form):
    bot_catcher = forms.CharField(
        required=False,
        widget=forms.HiddenInput)

    def clean_bot_catcher(self):
        value = self.cleaned_data['bot_catcher']
        if len(value) > 0:
            raise forms.ValidationError("Ботче а?")
        return value


class SignUpForm(UserCreationForm, AuthBotCatcherMixin):
    error_messages = {
        'password_mismatch': 'Паролите не съвпадат!'
    }

    password1 = forms.CharField(
        label='Парола',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                'class': 'u-form-group u-form-name u-block-4fcb-50 u-radius-16',
                'placeholder': 'Въведете парола',
            }
        ),
    )
    password2 = forms.CharField(
        label='Повторете паролата',
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                'class': 'u-form-group u-form-name u-block-4fcb-50 u-radius-16',
                'placeholder': 'Въведете паролата отново',
            }
        ),
        strip=False,
    )

    class Meta:
        model = UserModel
        fields = ['email']
        labels = {
            'email': 'Email'
        }
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Въведете email',
                    'class': 'u-form-group u-form-name u-block-4fcb-50 u-radius-16',
                }
            ),
        }


class SignInForm(AuthenticationForm, AuthBotCatcherMixin):
    error_messages = {
        "invalid_login": "Моля въведете коректен email и/или парола.",
    }

    username = UsernameField(
        label="E-mail",
        widget=forms.TextInput(
            attrs={
                'class': 'u-grey-5 u-input u-input-rectangle u-block-4fcb-52 u-radius-16',
                'placeholder': 'Въведете e-mail',
                'autofocus': True,

            }
        ),
    )

    password = forms.CharField(
        label='Парола',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "u-grey-5 u-input u-input-rectangle u-block-4fcb-55 u-radius-16",
                'placeholder': 'Въведете парола',
            }
        ),
    )


class ResetPasswordForm(SetPasswordForm):
    error_messages = {
        "invalid_login": "Моля въведете коректен email и/или парола.",
        'password_mismatch': 'Паролите не съвпадат!',
    }

    new_password1 = forms.CharField(
        label="Парола",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label="Повторете паролата",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
