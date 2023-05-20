import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'Password must be at least one uppercase letter, '
            'one lowercase letter and one number. The lenght should be '
            'at least 8 characters.'),
            code='invalid',)


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your email')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['last_name'], 'Ex.: Doe')
        add_placeholder(self.fields['password'], 'Type your password')
        add_placeholder(self.fields['password2'], 'Repeat your password')

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        error_messages={
            'requires': 'Password must not be empty'
        },
        help_text=(
            'Password must be at least one uppercase letter, '
            'one lowercase letter and one number. The lenght should be '
            'at least 8 characters.'
        ),
        label='Password',
        validators=[strong_password]
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Password2'
    )

    class Meta:
        model = User
        # for all fiels use: fields = '__all__'
        fields = ['first_name',
                  'last_name',
                  'username',
                  'password',
                  'email',
                  ]
        # alter for all fields except first_name for example
        # exclude = ['first_name']

        # Setting the labels
        labels = {
            'username': 'Username',
            'first_name':  'First name',
            'last_name': 'Last name',
            'email': 'E-mail',

        }

        help_texts = {
            'email': 'The e-mail must be valid.',
        }

        error_messages = {
            'username': {
                'required': 'This field must not be empty.',
                'invalid': 'This field is invalid.',
            }
        }

    # validate own Django

    # when one field needs another field

    def clean(self):
        cleaned_data = super().clean()

        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'Password and password2 must be equal.',
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [password_confirmation_error,
                              'Another error'],
            }
            )
