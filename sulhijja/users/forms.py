from django import forms
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from .models import Datadiri

class UserForms(forms.ModelForm):
    class Meta:
        model = User    
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            "first_name" : forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder':'First Name',
                    'required':True 
                }),
            "last_name" : forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder':'Last Name',
                    'required':True 
                }),
            "email" :forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder':'Email',
                    'required':True                     
                }),
        }

class DatadiriForms(forms.ModelForm):
    class Meta:
        model = Datadiri
        fields = ('alamat', 'telp')
        widgets = {
            "alamat" : forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder':'Alamat',
                    'required':True 
                }),
            "telp" : forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder':'Telpon',
                    'required':True 
                }),
        }