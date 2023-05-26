
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
        # self.make_recipe()
        recipes = self.make_recipes_in_batch()

        # User opens the page
        self.browser.get(self.live_server_url)
        # She/He sees one input in the field of search with the text: Search for a recipe
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for a recipe"]'
        )
        # click in this input and type the term of search
        # "Recipe title 1" to find the recipe with the title
        # search_input.click()
        # search_input.send_keys('Recipe title 1')
        search_input.send_keys(recipes[0].title)
        search_input.send_keys(Keys.ENTER)

        self.sleep(6)
        # self.assertIn('No recipes found here!', body.text)
