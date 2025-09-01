from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'image', 'stock']

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False)
