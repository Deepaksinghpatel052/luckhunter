from django import forms
from .models import LsUserAddress

class LsAddressForm(forms.ModelForm):
    Country = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Country", 'name': 'Country'}))
    State = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "State", 'name': 'State'}))
    City = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "City", 'name': 'City'}))
    Zip_Code = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Zip Code", 'name': 'Zip_Code'}))
    Address_1 = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Address 1", 'name': 'Address_1'}))
    Address_2 = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Address 2", 'name': 'Address_2'}))
    Lend_Mark = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Lend Mark", 'name': 'Lend_Mark'}))

    class Meta:
        model = LsUserAddress
        fields = ['Country', 'State', 'City', 'Zip_Code', 'Address_1','Address_2', 'Lend_Mark']