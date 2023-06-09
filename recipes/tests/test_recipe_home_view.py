# from unittest import skip

from unittest.mock import patch

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


# para pular os testes
# @skip('mensagem porque eu estou pulando esses testes')
class RecipeHomeViewsTest(RecipeTestBase):

    # setUp is runned before of each test
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func.view_class, views.RecipeListViewHome)
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

    def test_recipe_home_is_paginated(self):
        self.make_recipes_in_batch(8)

        # substituted by patch of mock (imported by unitest)
        # the part of the code below can change the PER_PAGE for all tests
        # So this code below is not a good practice of programmation
        # import recipes
        # simulating the per_page value
        # recipes.views.PER_PAGE = 3

        # patch as context management
        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator

            # verify the amount of pages is equal to number of pages
            # should have in the total
            self.assertEqual(paginator.num_pages, 3)

            # takes all the recipes on a page and compares them
            #  to the total amount that should be on each page.

            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 2)

    def test_invalid_page_query_uses_page_one(self):

        self.make_recipes_in_batch(8)
        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home')+'?page=1A')

            self.assertEqual(response.context['recipes'].number, 1)

            response = self.client.get(reverse('recipes:home')+'?page=2')

            self.assertEqual(response.context['recipes'].number, 2)

            response = self.client.get(reverse('recipes:home')+'?page=3')

            self.assertEqual(response.context['recipes'].number, 3)
