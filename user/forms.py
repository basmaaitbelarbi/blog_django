from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserCreationForm(forms.ModelForm):
    username = forms.CharField(label='username', max_length=30,
                               help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.')
    email_address = forms.EmailField(label='email_address')
    first_name = forms.CharField(label='first_name')
    last_name = forms.CharField(label='last_name')
    password1 = forms.CharField(
        label='password', widget=forms.PasswordInput(), min_length=8, help_text='Your password must contain at least 8 characters.')
    password2 = forms.CharField(
        label='password', widget=forms.PasswordInput(), min_length=8, help_text='Enter the same password as before, for verification.')

    class Meta:
        model = User
        fields = ('username', 'email_address', 'first_name',
                  'last_name', 'password1', 'password2')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('The two password fields didn’t match.')
        return cd['password2']

    def clean_username(self):
        cd = self.cleaned_data
        if User.objects.filter(username=cd['username']).exists():
            raise forms.ValidationError('A user with that username already exists.')
        return cd['username']

class LoginForm(forms.ModelForm):
    username =forms.CharField(label='username', max_length=15)
    password = forms.CharField(label='password',widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='first_name')
    last_name = forms.CharField(label='last_name')
    email_address = forms.EmailField(label='email_address')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email_address')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image',)

