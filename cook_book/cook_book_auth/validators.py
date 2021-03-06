from django.contrib.auth.password_validation import NumericPasswordValidator, CommonPasswordValidator, \
    MinimumLengthValidator
from django.core.exceptions import ValidationError


class NumericPasswordValidatorCustom(NumericPasswordValidator):
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError("Вашата парола не трябва да е само от цифри.")


class CommonPasswordValidatorCustom(CommonPasswordValidator):
    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError("Паролата е често срещана.")


class MinimumLengthValidatorCustom(MinimumLengthValidator):
    def __init__(self, min_length=5):
        super().__init__(min_length)
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(f'Паролата трябва да съдържа минимум {self.min_length} символа.')
