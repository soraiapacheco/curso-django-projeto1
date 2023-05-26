
from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here!', body.text)

    @patch('recipes.views.PER_PAGE', new=2)  # 2 recipes by page
    def test_recipe_search_input_can_find_correct_recipes(self):
        # creating the recipe
        recipes = self.make_recipes_in_batch()

        title_needed = 'This is what I need'
        recipes[0].title = title_needed
        recipes[0].save()

        # User opens the page
        self.browser.get(self.live_server_url)
        # She/He sees one input in the field of search with the text: Search for a recipe
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for a recipe"]'
        )
        # click in this input and type the term of search
        # to find the recipe with the title wanted
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        # The user sees what was looking for on the page
        self.assertIn(title_needed,
                      self.browser.find_element(
                          By.CLASS_NAME,
                          'main-content-list').text)
        self.sleep(6)

    @patch('recipes.views.PER_PAGE', new=2)  # 2 recipes by page
    def test_recipe_home_page_pagination(self):
        # creating the recipe
        recipes = self.make_recipes_in_batch()

        # User opens the page
        self.browser.get(self.live_server_url)

        # See what has one pagination and type on the page 2
        pagination = self.browser.find_element(
            By.XPATH,
            '//nav[@role="navigation"]'
        )
        self.sleep(6)