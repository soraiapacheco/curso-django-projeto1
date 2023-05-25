
from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By

from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    @patch('recipes.views.PER_PAGE', new=2)  # 2 recipes by page
    def test_recipe_home_without_recipes_not_found_message(self):
        # self.make_recipe()
        # self.make_recipes_in_batch(20)
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        # self.sleep()
        self.assertIn('No recipes found here!', body.text)
