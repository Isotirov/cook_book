from django import test as d_test_case
from django.contrib.auth import get_user_model
from django.urls import reverse

from cook_book.cook_book_main_app.models import CookedMeal

UserModel = get_user_model()


class CookedMealViewTests(d_test_case.TestCase):
    VALID_USER_DATA = {
        'email': 'van@van.com',
        'password': 'marata'
    }

    VALID_MEAL_DATA = {
        'type': CookedMeal.STARTER,
        'title': 'food',
        'ingredients': 'spice',
        'cooking_time': 30,
        'description': 'cooked',
    }

    ANOTHER_VALID_MEAL_DATA = {
        'type': CookedMeal.SWEET,
        'title': 'sweet_food',
        'ingredients': 'sugar',
        'cooking_time': 30,
        'description': 'cooked',
    }

    def __create_meal(self):
        user = UserModel.objects.create(**self.VALID_USER_DATA)
        meal = CookedMeal.objects.create(**self.VALID_MEAL_DATA, user=user)

        return meal

    def __create_user(self):
        user = UserModel.objects.create(**self.VALID_USER_DATA)

        return user

    def test_get__expect_correct_template(self):
        response = self.client.get(reverse('landing page'))

        self.assertTemplateUsed(response, 'landing_page.html')

    # def test_not_valid_url__expect_404(self):
    #     response = self.client.get(reverse('recipe details', kwargs={'pk': 1}))
    #
    #     self.assertEqual(404, response.status_code)

    def test_when_two_recipes__expect_two_recipes(self):
        user = self.__create_user()

        recipes_to_create = (
            CookedMeal(**self.VALID_MEAL_DATA, user=user),
            CookedMeal(**self.ANOTHER_VALID_MEAL_DATA, user=user)
        )

        CookedMeal.objects.bulk_create(recipes_to_create)

        response = self.client.get(reverse('all recipes'))

        recipes = response.context['object_list']

        self.assertEqual(len(recipes), 2)

    def test_queryset_contains_one_object__expect_to_return_only_one_object(self):
        user = self.__create_user()

        recipes_to_create = (
            CookedMeal(**self.VALID_MEAL_DATA, user=user),
            CookedMeal(**self.ANOTHER_VALID_MEAL_DATA, user=user)
        )

        CookedMeal.objects.bulk_create(recipes_to_create)

        response = self.client.get(reverse('starters'))

        expected_result = response.context['object_list']

        self.assertEqual(len(expected_result), 1)
