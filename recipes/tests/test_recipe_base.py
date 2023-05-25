from django.test import TestCase

from recipes.models import Category, Recipe, User


# Mixing is a pattern project that is one class that is one bag of methods
class RecipeMixing:
    def make_category(self, name='Category'):
        return Category.objects.create(name=name)

    def make_author(self,
                    first_name='user',
                    last_name='name',
                    username='username',
                    password='123456',
                    email='username@email.com'

                    ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email)

    def make_recipe(self,
                    category_data=None,
                    author_data=None,
                    title='Recipe Title',
                    description='Recipe Description',
                    slug='recipe-slug',
                    preparation_time=10,
                    preparation_time_unit='Minutos',
                    servings=5,
                    servings_unit='Porções',
                    preparation_steps='Recipe Preparation Steps',
                    preparation_steps_is_html=False,
                    is_published=True
                    ):
        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return Recipe.objects.create(
            category=self.make_category(**category_data),
            # ** expand the dictionary
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published)

    def make_recipes_in_batch(self, qtd=10):
        recipes = []
        for i in range(qtd):
            kwargs = {'author_data': {'username': f'u{i}'}, 'slug': f'r{i}'}
            recipe = self.make_recipe(**kwargs)
            recipes.append(recipe)
        return recipes

# # Python allows multiple inheritance


class RecipeTestBase(TestCase, RecipeMixing):
    def setUp(self) -> None:
        return super().setUp()
