
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthorLogoutTest(TestCase):
    def test_user_tries_to_logou_using_get_method(self):
        User.objects.create_user(username='my_user', password='my_password')
        self.client.login(username='my_user', password='my_password')
        # follow in the redirect to not return empty the response
        response = self.client.get(reverse('authors:logout'),
                                   follow=True)

        # This response is empty without follow parameter in the command
        # previously because this method return one redirect and stop
        print('NOSSO RESPONSE: ', response.content.decode('utf-8'))
