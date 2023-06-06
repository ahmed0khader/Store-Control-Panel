from dataclasses import fields
from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields =['product', 'status', 'note']
        
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']
        
# register
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2']