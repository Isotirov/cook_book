from django import test as d_test_case
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from cook_book.cook_book_profiles.models import CookBookUserProfile


UserModel = get_user_model()


class CookBookUserProfilesTests(d_test_case.TestCase):
    VALID_USER_DATA = {
        'email': 'van@van.bg',
        'password': 'test'
    }

    VALID_PROFILE_DATA = {
        'first_name': 'Ivan',
        'last_name': 'Sotirov',
        'joined': '2022-04-14'
    }

    def test_profile_create__when_first_name_last_name_contain_only_letters__expect_success(self):
        user = UserModel(**self.VALID_USER_DATA)
        user.save()
        profile = CookBookUserProfile(**self.VALID_PROFILE_DATA, user=user)
        profile.save()

    def test_profile_create__profile_full_name__expect_correct(self):
        user = UserModel(**self.VALID_USER_DATA)
        user.save()
        profile = CookBookUserProfile(**self.VALID_PROFILE_DATA, user=user)
        profile.save()

        expected_name = f'{self.VALID_PROFILE_DATA["first_name"]} {self.VALID_PROFILE_DATA["last_name"]}'

        self.assertEqual(expected_name, str(profile))

    def test_profile_create__when_first_name_does_not_contains_only_letters__expect_failure(self):
        first_name = 'Ivan1'
        user = UserModel(**self.VALID_USER_DATA)
        user.save()
        profile = CookBookUserProfile(
            first_name=first_name,
            last_name=self.VALID_PROFILE_DATA["last_name"],
            joined=self.VALID_PROFILE_DATA["joined"],
            user=user
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_all_data_entered_is_complete_true__expect_true(self):
        user = UserModel(**self.VALID_USER_DATA)
        user.save()

        profile = CookBookUserProfile(**self.VALID_PROFILE_DATA, user=user)
        profile.save()

        self.assertEqual(True, profile.is_complete)

    def test_profile_create__when_not_all_data_entered_is_complete__expect_false(self):
        user = UserModel(**self.VALID_USER_DATA)
        user.save()

        profile = CookBookUserProfile(
            first_name=self.VALID_PROFILE_DATA["first_name"],
            joined=self.VALID_PROFILE_DATA["joined"],
            user=user)
        profile.save()

        self.assertEqual(False, profile.is_complete)
