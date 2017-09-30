from django import forms
from django.contrib.auth.models import User

from .models import Boutique, Product


class BoutiqueForm(forms.ModelForm):

    class Meta:
        model = Boutique
        fields = ['shop_name']


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['product_name', 'product_img','product_price','product_desc']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
