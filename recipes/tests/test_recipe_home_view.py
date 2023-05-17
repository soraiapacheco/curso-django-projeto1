# from unittest import skip

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


# para pular os testes
# @skip('mensagem porque eu estou pulando esses testes')
class RecipeHomeViewsTest(RecipeTestBase):

    # setUp is runned before of each test
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)
    # tearDown is runned after of each test

    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    # WIP = Wokr in progress
    # @skip('WIP')
    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1>No recipes found here!</h1>',
            response.content.decode('utf-8'))

        # Supose that I write more test and I want to stop here
        # I can cause the fail function of the test, for example
        # self.fail('Para eu terminar de digitar o que falta')

    def test_recipe_home_templates_loads_recipes(self):
        # Other way to create category, but it is necessary to
        #  include the command save()
        # category = Category(name='Category')
        # category.full_clean()
        # category.save()
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        self.assertIn('Recipe Title', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_templates_dont_load_recipes_not_published(self):
        """Test for recipe that will be showed"""
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))
        self.assertIn('<h1>No recipes found here!</h1>',
                      response.content.decode('utf-8'))

    def test_recipe_home_templates_qtd_items_within_page(self):
        """Test for recipe that will be showed"""
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))
        response_context_recipes = response.context['recipes']
        per_page = response_context_recipes.paginator.per_page

        self.assertEqual(9, per_page)
