from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import AuthorBaseTest


class AuthorsRegisterTest(AuthorBaseTest):
    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(By.XPATH,
                                        f'//input[@placeholder="{placeholder}"]')

    def test_the_test(self):
        self.browser.get(self.live_server_url + '/authors/register')
        form = self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )
        first_name_field = self.get_by_placeholder(form, 'Ex.: John')
        first_name_field.send_keys('ATENÇÃO')
        first_name_field.send_keys(Keys.ENTER)

        self.sleep(5)
