from cloudinary import models as cloudinary_model
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

from cook_book.cook_book_profiles.validators import only_letters_validator

UserModel = get_user_model()


class CookBookUserProfile(models.Model):
    FIRST_NAME_MAX_LENGTH = 15
    FIRST_NAME_MIN_LENGTH = 2
    LAST_NAME_MAXLENGTH = 15
    LAST_NAME_MIN_LENGTH = 2
    MAX_FILE_SIZE = 5
    MIN_LENGTH_ERROR_MESSAGE = 'Името трябва да съдържа поне две букви!'

    image = cloudinary_model.CloudinaryField('image')
    #         (
    #     upload_to='profile_pictures',
    #     default='profile_pictures/default_profile_image.png',
    #     validators=[FileMaxSizeMBValidator(MAX_FILE_SIZE)],
    # )

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        default='Нов',
        validators=[MinLengthValidator(FIRST_NAME_MIN_LENGTH), only_letters_validator],
        error_messages={
            'min_length': MIN_LENGTH_ERROR_MESSAGE,
        }
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAXLENGTH,
        default='Потребител',
        validators=[MinLengthValidator(LAST_NAME_MIN_LENGTH), only_letters_validator],
        error_messages={
            'min_length': MIN_LENGTH_ERROR_MESSAGE,
        }
    )

    joined = models.DateField(
        auto_now_add=True,
    )

    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    is_complete = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
