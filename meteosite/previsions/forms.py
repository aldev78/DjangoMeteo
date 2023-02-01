from crispy_bulma.layout import Row, Column, Submit
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django import forms
from .models import Departement
from django.forms import ModelChoiceField


class DepartementModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.nom


class VilleForm(forms.Form):
    nom = forms.CharField(label='Nom', max_length=60, required=True)
    code_postal = forms.IntegerField(widget=forms.TextInput, label="Code postal", required=True)
    departement = DepartementModelChoiceField(label="Département",
                                              required=True,
                                              queryset=Departement.objects.all(),
                                              empty_label="(Choisir un département)",
                                              )


class DepartClientForm(forms.Form):
    departement = DepartementModelChoiceField(label="Département",
                                              required=True,
                                              queryset=Departement.objects.all(),
                                              empty_label="(Choisir un département)",
                                              widget=forms.Select(attrs={'onchange': 'submit();'},),
                                              )

