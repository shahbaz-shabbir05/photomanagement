from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext, ugettext_lazy as _


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required.')
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput, help_text='Password.')
    password2 = forms.CharField(label=_("Confirm Password"), widget=forms.PasswordInput,
                                help_text=_("Enter the same Password as above."))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

    # def __init__(self, *args, **kwargs):
    #     super(SignUpForm, self).__init__(*args, **kwargs)
    #
    #     for fieldname in ['username', 'email']:
    #         self.fields[fieldname].help_text = None

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2


class SignInForm(AuthenticationForm):
    username = UsernameField(max_length=254, widget=forms.TextInput(attrs={'autofocus': True, }), help_text='Required.')
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput, help_text='Required.')

    class Meta:
        model = User

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                "This account is inactive.",
                code='inactive',
            )
