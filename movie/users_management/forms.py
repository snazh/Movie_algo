from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from .models import UserProfile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')  # Add other fields as needed

    def clean_username(self):  # custom validator
        username = self.cleaned_data['username']
        if len(username) < 5:
            raise ValidationError('Too short username')
        elif len(username) > 30:
            raise ValidationError('Too long username')
        return username

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

            # Create UserProfile
            UserProfile.objects.create(
                user=user,
                first_name='',
                last_name='',
                bio='',
                slug=slugify(self.cleaned_data['username']),
                avatar=''  # You can adjust this field as needed
            )

        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.PasswordInput()


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'bio', 'avatar')

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'type': "text", 'value': 'first_name' }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'type': "text", 'value': 'last_name'}
        )
    )
    bio = forms.CharField(
        widget=forms.Textarea(
            attrs={'cols': "55", 'rows': "5", 'style': "resize: none;", 'value': 'bio '}
        )
    )
    avatar = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={'class': 'input_text'}
        )
    )

    def clean_first_name(self):  # custom validator
        first_name = self.cleaned_data['first_name']
        if len(first_name) < 5:
            raise ValidationError('Too short name')
        if len(first_name) > 30:
            raise ValidationError('Too long name')
        return first_name

    def clean_last_name(self):  # custom validator
        last_name = self.cleaned_data['last_name']
        if len(last_name) < 5:
            raise ValidationError('Too short last name')
        if len(last_name) > 30:
            raise ValidationError('Too long last name')
        return last_name

    def clean_bio(self):
        bio = self.cleaned_data['bio']
        if len(bio) > 5000:
            raise ValidationError('Too long biography')
        return bio
