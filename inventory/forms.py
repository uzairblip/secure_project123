from django import forms
from .models import Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# ==========================================
# 1. PRODUCT FORM (Your Existing Code)
# ==========================================
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'quantity', 'price']

    # This function runs automatically to BLOCK negative numbers
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError("Ensure this value is greater than or equal to 0.")
        return price

# ==========================================
# 2. SIGNUP FORM (New - Adds Email Field)
# ==========================================
class SignUpForm(UserCreationForm):
    # This adds the Email box to the form and makes it mandatory
    email = forms.EmailField(required=True, help_text="Required. We will send a 2FA token here.")

    class Meta:
        model = User
        # We specify that we want both Username and Email to appear
        fields = ('username', 'email')