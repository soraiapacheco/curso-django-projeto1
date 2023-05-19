from django import forms
from django.contrib.auth.models import User


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your email')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['last_name'], 'Ex.: Doe')
        add_attr(self.fields['username'], 'css', 'a-css-class')

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password'
        }),
        error_messages={
            'requires': 'Password must not be empty'
        },
        help_text=(
            'Password must be at least one uppercase letter, '
            'one lowercase letter and one number. The lenght should be '
            'at least 8 characters.'
        )
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password'
        })
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
