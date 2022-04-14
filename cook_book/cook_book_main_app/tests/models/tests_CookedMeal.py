from django import test as d_test_case
from django.contrib.auth import get_user_model

from cook_book.cook_book_main_app.models import CookedMeal


UserModel = get_user_model()


class CookedMealTests(d_test_case.TestCase):
    VALID_USER_DATA = {
        'email': 'van@van.bg',
        'password': 'test'
    }

    VALID_MEAL_DATA = {
        'type': CookedMeal.STARTER,
        'title': 'food',
        'ingredients': 'spice',
        'description': 'cooked',
    }

    def test_format_cooking_time_less_than_sixty_minutes(self):
        cook_time = 59
        user = UserModel(**self.VALID_USER_DATA)
        user.save()

        meal = CookedMeal(
            **self.VALID_MEAL_DATA,
            cooking_time=cook_time,
            user=user
        )
        meal.save()

        expected_time_format = f'{59} мин.'

        self.assertEqual(expected_time_format, meal.format_cooking_time())

    def test_format_cooking_time_more_than_sixty_minutes_and_not_round_the_clock(self):
        cook_time = 70
        user = UserModel(**self.VALID_USER_DATA)
        user.save()

        meal = CookedMeal(
            **self.VALID_MEAL_DATA,
            cooking_time=cook_time,
            user=user
        )
        meal.save()

        expected_time_format = f'{cook_time // 60} ч. и {cook_time % 60} мин.'

        self.assertEqual(expected_time_format, meal.format_cooking_time())

    def test_format_cooking_time_more_than_sixty_minutes_and_round_the_clock(self):
        cook_time = 60
        user = UserModel(**self.VALID_USER_DATA)
        user.save()

        meal = CookedMeal(
            **self.VALID_MEAL_DATA,
            cooking_time=cook_time,
            user=user
        )
        meal.save()

        expected_time_format = f'{cook_time // 60} ч.'

        self.assertEqual(expected_time_format, meal.format_cooking_time())
