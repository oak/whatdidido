# -*- coding: utf-8 -*-
__author__ = 'adcarvalho'
from django import forms
import autocomplete_light
from web.models import Action, Thing


class QuickActionForm(forms.Form):
    thing = forms.CharField(required=True,
                            widget=autocomplete_light.TextWidget('ThingAutocomplete', attrs={'class': 'form-control', },
                                                                 autocomplete_js_attributes={
                                                                 'placeholder': u'I...'}, ), )

class EditActionForm(forms.ModelForm):
    date = forms.DateTimeField(required=True, widget=forms.DateTimeInput)
    class Meta:
        model = Action
        exclude = ('thing', 'user', )