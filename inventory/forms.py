from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'quantity', 'price']
        # This tells Django: "Build a form automatically based on these 3 database columns"