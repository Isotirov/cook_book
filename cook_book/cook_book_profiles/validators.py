from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


def only_letters_validator(value):
    if not any(ch.isalpha() for ch in value):
        raise ValidationError('Името трябва да съдържа само букви!')


@deconstructible
class FileMaxSizeMBValidator:
    def __init__(self, max_size_mb):
        self.max_size_mb = max_size_mb

    def __call__(self, value, *args, **kwargs):
        if value.file.size > self.max_size_mb * 1024 * 1024:
            raise ValidationError(f'Изображението надвишава максимално допустимия размер ({self.max_size_mb} MB)!')