# -*- coding: utf-8 -*-
__author__ = 'adcarvalho'
from django import forms
from web.models import Thing


class ThingForm(forms.ModelForm):
    class Meta:
        model = Thing
        exclude = ('owner',)