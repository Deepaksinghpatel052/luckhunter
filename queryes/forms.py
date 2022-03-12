from django import forms
from .models import LsQerues

class LsQeruesForm(forms.ModelForm):
    Title = forms.CharField(required=False, widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Title", 'name': 'Title'}))
    description = forms.CharField(required=False, widget=forms.Textarea(
        attrs={"class": "form-control login-frm-input", "style": "height: 100px!important;    padding: 11px;",
               "placeholder": "Description", 'name': 'description'}))
    class Meta:
        model = LsQerues
        fields = ['Title', 'description']
