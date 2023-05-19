from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
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
            'password': 'Password',
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

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your first name here.',
                'class': 'input text-input outra-classe',
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password here.',
            })
        }
