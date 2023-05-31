# from unittest import skip

from unittest.mock import patch

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
        self.assertIs(view.func.view_class, views.RecipeListViewCategory)

    def test_recipe_category_view_returns_404_is_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_view_is_paginated(self):
        for i in range(8):
            kwargs = {'author_data': {'username': f'u{i}'}, 'slug': f'r{i}'}
            self.make_recipe(**kwargs)

        # substituted by patch of mock (imported by unitest)
        # the part of the code below can change the PER_PAGE for all tests
        # So this code below is not a good practice of programmation
        # import recipes
        # simulating the per_page value
        # recipes.views.PER_PAGE = 3

        # patch as context management
        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(
                reverse('recipes:category', kwargs={'category_id': 1}))
            recipes = response.context['recipes']
            paginator = recipes.paginator

            # verify the amount of pages is equal to number of pages
            # should have in the total
            self.assertEqual(paginator.num_pages, 1)
