# -*- coding: utf-8 -*-
__author__ = 'adcarvalho'

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={}), label=u'User')
    password = forms.CharField(widget=forms.PasswordInput(attrs={}), label=u'Password')
