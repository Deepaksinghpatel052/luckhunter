from django import forms
from .models import LsBlog
from products.models import LsProduct


class LsBlogForm(forms.ModelForm):
    Blog_Title = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Blog Title", 'name': 'Blog_Title'}))
    Blog_Contect = forms.CharField( widget=forms.Textarea(attrs={"class": "form-control", 'name': 'Blog_Contect', 'placeholder': "Blog Contect"}))
    Blog_description = forms.CharField( widget=forms.Textarea(attrs={"class": "form-control", 'name': 'Blog_description', 'placeholder': "Blog description"}))
    class Meta:
        model = LsBlog
        fields = ['product', 'Blog_Title', 'Blog_Contect', 'Blog_description']

    def __init__(self, user_ins, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'] = forms.ModelChoiceField(required=False,empty_label="Please select Product",queryset=LsProduct.objects.all(),widget=forms.Select(attrs={"class": "form-control"}))