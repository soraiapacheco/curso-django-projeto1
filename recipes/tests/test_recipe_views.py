from unittest import skip

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


# para pular os testes
# @skip('mensagem porque eu estou pulando esses testes')
class RecipeViewsTest(RecipeTestBase):

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
        # Other way to create category, but it is necessary to include the command save()
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
            reverse('recipes:category', kwargs={'category_id': recipe.category.id}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_is_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)

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
