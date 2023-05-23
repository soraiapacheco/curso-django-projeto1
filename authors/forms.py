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

    username = forms.CharField(
        error_messages={
            'required': 'This field must not be empty.',
            'invalid': 'This field is invalid.',
            'min_length': 'Username must have at least 4 characters.',
            'max_length': 'Username must have less than 150 characters.'
        },

        required=True,
        label='Username',
        help_text=(
            'Username must have letter, numbers or one of those @.+-_'
            '. The lenght should be between 4 and 150 characters.'
        ),
        min_length=4, max_length=150,
    )

    first_name = forms.CharField(
        error_messages={'required': 'Write your first name'},
        required=True,
        label='First name'
    )

    last_name = forms.CharField(
        error_messages={'required': 'Write your last name'},
        required=True,
        label='Last name'
    )
    email = forms.EmailField(
        error_messages={'required': 'Email is required'},
        required=True,
        label='E-mail',
        help_text='The e-mail must be valid.',

    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Password must not be empty'
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
        label='Password2',
        error_messages={
            'required': 'Please, repeat your password'
        },
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

        error_messages = {
            'username': {
                'required': 'This field must not be empty.',
                'invalid': 'This field is invalid.',
            }
        }

    # validate own Django

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'User e-mail is already in use', code='invalid'
            )

        return email

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

        return cleaned_data
