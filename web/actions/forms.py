# -*- coding: utf-8 -*-
__author__ = 'adcarvalho'
from django import forms
import autocomplete_light
from web.models import Action, Thing


class ActionForm(forms.Form):
    thing = forms.CharField(required=True, widget=autocomplete_light.TextWidget('ThingAutocomplete'), )