from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm

UserModel = get_user_model()


class SignUpForm(UserCreationForm):
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


class SignInForm(AuthenticationForm):
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
