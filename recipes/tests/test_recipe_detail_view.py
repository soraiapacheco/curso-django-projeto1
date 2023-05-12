# from unittest import skip

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


# para pular os testes
# @skip('mensagem porque eu estou pulando esses testes')
class RecipeDetailViewsTest(RecipeTestBase):
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_is_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_templates_is_correct(self):
        needed_title = 'This is a detail page. It load one recipe'

        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:recipe',
                                   kwargs={'id': 1
                                           }))
        content = response.content.decode('utf-8')

        self.assertIn(needed_title, content)

    def test_recipe_detail_templates_dont_load_recipe_not_published(self):
        """Test for recipe that will be showed if the detail doesnt exist"""
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse('recipes:recipe',
                    kwargs={'id': recipe.id}))

        self.assertEqual(response.status_code, 404)
