import pytest
from django.contrib.auth.models import User
from django.urls import reverse  # dynamic url
from selenium.webdriver.common.by import By

from .base import AuthorBaseTest


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorBaseTest):
    def test_user_valid_data_can_login_sucessfully(self):
        # Creating the user objects with data of the users
        string_password = 'pass'
        user = User.objects.create_user(
            username='my_user', password=string_password)

        # User opens of the login page
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # User sees the login form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        # User type your user and password
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        # User submmit the form
        form.submit()

        # User sees the msg of login with success and your name
        self.assertIn(
            f'Your are logged in with {user.username}.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

        # self.sleep(6)
        assert 1 == 1
