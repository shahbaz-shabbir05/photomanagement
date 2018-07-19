from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import HiddenInput
from django.template import Template
from django.utils.translation import ugettext_lazy as _

from photomanagementapp.models import Gallery, Photo


class SignUpForm(UserCreationForm):
    username = UsernameField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username', 'autofocus': True, }), help_text='Username.')

    first_name = forms.CharField(widget=(forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})),
                                 max_length=30, required=False, help_text='Optional.')

    last_name = forms.CharField(widget=(forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})),
                                max_length=30, required=False, help_text='Optional.')

    email = forms.EmailField(widget=(forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'})),
                             max_length=254, help_text='Required.')

    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
                                help_text='Password.')

    password2 = forms.CharField(label=_("Confirm Password"),
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
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
    username = UsernameField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username', 'autofocus': True, }), help_text='Username.')

    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
                               help_text='Password.')

    class Meta:
        model = User

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                "This account is inactive.",
                code='inactive',
            )


class GalleryCreationForm(forms.ModelForm):
    title = forms.CharField(widget=(forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Gallery Name'})),
                            max_length=100, required=False, help_text='Enter Gallery Name.')
    description = forms.CharField(
        widget=(forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Gallery Description'})), required=False,
        help_text='Gallery Description.')

    class Meta:
        model = Gallery
        fields = ('title', 'description')

    def clean_title(self):
        title = self.cleaned_data['title']
        r = Gallery.objects.filter(title=title)
        if r.count():
            raise ValidationError("Gallery title should be unique.")
        return title


class UploadPhotoForm(forms.ModelForm):
    title = forms.CharField(widget=(forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Photo Name'})),
                            max_length=200, required=False, help_text='Enter Photo Name..')
    image = forms.ImageField(widget=forms.FileInput)

    description = forms.CharField(
        widget=(forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Photo Description'})), required=False,
        help_text='Photo Description.')

    def __init__(self, *args, **kwargs):
        gallery_id = kwargs.pop('gallery_id', None)
        super(UploadPhotoForm, self).__init__(*args, **kwargs)
        if gallery_id:
            self.fields['gallery'].initial = gallery_id
            self.fields['gallery'].widget = HiddenInput()

    class Meta:
        model = Photo
        fields = ('title', 'description', 'image', 'gallery')
