from django.core.exceptions import ValidationError

from .test_recipe_base import RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def test_recipe_title_raise_error_if_title_more_than_65_chars(self):
        self.recipe.title = 'A' * 70
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_max_length(self):
        fields = [
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65)

        ]
        for field, max_length in fields:
            with self.subTest(field=field, max_length=max_length):
                # attribution dynamic for recipe variable
                setattr(self.recipe, field, 'A' * (max_length+1))
                with self.assertRaises(ValidationError):
                    self.recipe.full_clean()
