from captcha.fields import CaptchaField
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Team


class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form_input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form_input'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form_input'}))
    slug = forms.CharField(label='URL', widget=forms.TextInput(attrs={'class': 'form_input'}))
    signup_captcha = CaptchaField(label="")

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'slug', 'signup_captcha')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form_input'}),
            'password': forms.PasswordInput(attrs={'class': 'form_input'}),
            'slug': forms.TextInput(attrs={'class': 'form_input'}),
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form_input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form_input'}))


class CreateTeamForm(ModelForm):
    signup_captcha = CaptchaField(label="")
    class Meta:
        model = Team
        fields = ['short_name', 'long_name', 'slug', 'photo', 'signup_captcha']


class EditTeamForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.team_id = kwargs.pop('team_id')
        super(EditTeamForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Team
        fields = ['short_name', 'long_name', 'slug', 'photo']
        #widgets = {'id': forms.HiddenInput()}

    def clean_short_name(self):  # Сделать редактирование команды !!!!!
        short_name = self.cleaned_data['short_name']
        if Team.objects.filter(short_name=short_name).exclude(pk=self.team_id).exists():
            print(Team.objects.filter(short_name=short_name).exclude(pk=self.team_id))
            return ValidationError('Команда с таким коротким названием уже существует')
        print(Team.objects.filter(short_name=short_name).exclude(pk=self.team_id))
        return short_name
    
    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if Team.objects.filter(slug=slug).exclude(pk=self.team_id).exists():
            print(Team.objects.filter(slug=slug).exclude(pk=self.team_id))
            return ValidationError('Команда с таким коротким названием уже существует')
        print(Team.objects.filter(slug=slug).exclude(pk=self.team_id))
        return slug



