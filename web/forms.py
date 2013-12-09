# -*- coding: utf-8 -*-
__author__ = 'adcarvalho'

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control', }), label=u'User', )
    password = forms.CharField(widget=forms.PasswordInput(attrs={ 'class': 'form-control', }), label=u'Password', )
