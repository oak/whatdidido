__author__ = 'adcarvalho'

import autocomplete_light
from web.models import Thing


class ThingAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['name', ]
    order_fields = ['usage_count', ]



autocomplete_light.register(Thing, ThingAutocomplete)