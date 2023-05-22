

# substituing TestCase of Django by TestCase of Python (unittest)
# due to faster
# from django.test import TestCase
from unittest import TestCase

from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized

from authors.forms import RegisterForm


class AuthorRegisterFormUnitTest(TestCase):

    @parameterized.expand([
        ('username', 'Your username'),
        ('email', 'Your email'),
        ('first_name', 'Ex.: John'),
        ('last_name', 'Ex.: Doe'),
        ('password', 'Type your password'),
        ('password2', 'Repeat your password'),

    ])
    def test_fields_placeholder(self, field, needed):
        form = RegisterForm()
        current = form[field].field.widget.attrs['placeholder']
        self.assertEqual(needed, current)

    @parameterized.expand([
        ('username', (
            'Obrigatório. 150 caracteres ou menos. '
            'Letras, números e @/./+/-/_ apenas.')
         ),
        ('email', 'The e-mail must be valid.'),
        ('password', (
            'Password must be at least one uppercase letter, '
            'one lowercase letter and one number. The lenght should be '
            'at least 8 characters.')
         ),

    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(needed, current)

    @parameterized.expand([
        ('username', 'Username'),
        ('first_name',  'First name'),
        ('last_name', 'Last name'),
        ('email', 'E-mail'),
        ('password', 'Password'),
        ('password2', 'Password2'),

    ])
    def test_fields_labels(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(needed, current)


class AuthorRegisterFormIntegratioTest(DjangoTestCase):
    def setUp(self, *args, **kwargs) -> None:
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@anyemail.com',
            'password': 'Str0ngP@ssword1',
            'password2': 'Str0ngP@ssword1',
        }

        return super().setUp(*args, **kwargs)

    @parameterized.expand([('username', 'This field must not be empty.'),
                           ('first_name', 'Write your first name'),
                           ('last_name', 'Write your last name'),
                           ('password', 'Password must not be empty'),
                           ('password2', 'Please, repeat your password'),
                           ('email', 'Email is required'),

                           ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        # verify the url
        url = reverse('authors:create')

        # verifty the post of page
        # follow means to follow the redirect within
        # register_create in urls of author
        response = self.client.post(url, data=self.form_data, follow=True)

        # identify if the message is within the content of the page
        self.assertIn(msg, response.content.decode('utf-8'))

        # to easy the read it uses the command below, you should
        #  comment the line above
        self.assertIn(msg, response.context['form'].errors.get(field))
