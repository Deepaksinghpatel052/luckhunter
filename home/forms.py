from django import forms
from .models import lsUserProduct



class lsUserProductForm(forms.ModelForm):
    Your_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", 'name': 'Your_name','placeholder':'Your name'}))
    Email = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", 'name': 'Email','placeholder':'Email'}))
    Contact_no = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", 'name': 'Contact_no','placeholder':'Contact No.'}))
    Product_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", 'name': 'Product_name', 'placeholder':'Product Name'}))
    Product_URL = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", 'name': 'Product_URL' ,'placeholder':"Product URL"}))

    class Meta:
        model = lsUserProduct
        fields = ['Your_name','Email','Contact_no','Product_name','Product_URL']
