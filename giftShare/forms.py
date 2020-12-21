from django import forms
from django.forms import ModelForm, TextInput
from django.utils.translation import gettext_lazy as _
from .models import GLUser, Gift

class RegisterUsername(ModelForm):
    class Meta:
      model = GLUser
      fields = '__all__'
      labels = {
            'username': _('Username:'),
            'email': _('Email:'),
            'password': _('Password:'),
            'firstName': _('First Name:'),
            'lastName': _('Last Name:'),
        }
      widgets = {
          'password': TextInput(attrs={'type' : 'password'})
      }

class GiftForm(ModelForm):
    class Meta:
      model = Gift
      fields = ['name']
      labels = {
            'name': _('Name:')
        }
class SignInUserForm(forms.Form):
  username = forms.CharField(max_length=30, required=True)
  password = forms.CharField(widget=forms.TextInput(attrs={'type' : 'password'}))

