from django.contrib.auth import get_user_model
from django.db import models
from cloudinary import models as cloudinary_model

UserModel = get_user_model()


class CookedMeal(models.Model):
    _STARTER_TITLE_MAX_LENGTH = 30

    STARTER = 'Предястие'
    PASTA = 'Тестено изделие'
    CAKE = 'Торта'
    SWEET = 'Сладкиш'
    MEAL = 'Основно ястие'
    VEGAN = 'Веган'

    MEALS = [(x, x) for x in [STARTER, PASTA, CAKE, SWEET, MEAL, VEGAN]]

    type = models.CharField(
        max_length=max(len(x) for _, x in MEALS),
        choices=MEALS,
    )

    title = models.CharField(
        max_length=_STARTER_TITLE_MAX_LENGTH,
    )

    ingredients = models.TextField()

    cooking_time = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    description = models.TextField()

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def format_cooking_time(self):
        if self.cooking_time < 60:
            return f'{self.cooking_time} мин.'
        hour = self.cooking_time // 60
        minutes = self.cooking_time % 60
        if minutes > 0:
            return f'{hour} ч. и {minutes} мин.'
        return f'{hour} ч.'

    class Meta:
        unique_together = ['type', 'title', 'user']


class MealImage(models.Model):
    # _MAX_FILE_SIZE_MB = 5

    image = cloudinary_model.CloudinaryField('image')
    # (upload_to='pictures',
    # validators=[FileMaxSizeMBValidator(_MAX_FILE_SIZE_MB)],)

    meal = models.ForeignKey(
        CookedMeal,
        on_delete=models.CASCADE
    )


class Comment(models.Model):
    comment = models.TextField()

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )

    recipe = models.ForeignKey(
        CookedMeal,
        on_delete=models.CASCADE
    )


class Like(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )

    recipe = models.ForeignKey(
        CookedMeal,
        on_delete=models.CASCADE
    )
