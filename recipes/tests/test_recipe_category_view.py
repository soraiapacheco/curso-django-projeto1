# from unittest import skip

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


# para pular os testes
# @skip('mensagem porque eu estou pulando esses testes')
class RecipeCategoryViewsTest(RecipeTestBase):

    def test_recipe_category_templates_loads_recipes(self):
        needed_title = 'It is category test'

        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')

        self.assertIn(needed_title, content)

    def test_recipe_category_templates_dont_load_recipes_not_published(self):
        """Test for recipe that will be showed if the category doesnt exist"""
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse('recipes:category',
                    kwargs={'category_id': recipe.category.id}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_is_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)
