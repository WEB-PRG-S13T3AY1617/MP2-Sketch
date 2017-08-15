from django import forms
from django.db import models

choices = (('student', 'Student'), ('teacher', 'Teacher'))

# Create your models here.
class Account(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    password = models.CharField(max_length=150)
    cell = models.CharField(max_length=20, default="+00 000 000 0000")
    type = models.CharField(max_length=7, default='student', choices=choices)
    picture = models.ImageField(upload_to="users/", default="default.jpg")
    def __str__(self):
        return self.name
    
class LoginForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['username', 'password']

        widgets = {
            'username': forms.TextInput(attrs={'required': True, 'placeholder': 'Username...'}),
            'password': forms.PasswordInput(attrs={'required': True, 'placeholder': 'Password...'}),
        }

        labels = {
            'username': 'Username',
            'password': 'Password',
        }

class RegisterForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['name', 'email', 'username', 'password', 'type', 'cell', 'picture']

        widgets = {
            'name': forms.TextInput(attrs={'required': True, 'placeholder': 'Full Name...'}),
            'email': forms.EmailInput(attrs={'required': True, 'placeholder': 'Email Address...'}),
            'username': forms.TextInput(attrs={'required': True, 'placeholder': 'Desired Username...'}),
            'password': forms.PasswordInput(attrs={'required': True, 'placeholder': 'Desired Password...'}),
            'cell': forms.TextInput(attrs={'required': False, 'placeholder': '+00 000 000 0000'}),
        }

        labels = {
            'name': 'Name',
            'email': 'Email Address',
            'username': 'Username',
            'password': 'Password',
            'picture': 'Profile Picture',
            'cell': 'Cellphone Number',
            'type': 'Account Type',
        }
