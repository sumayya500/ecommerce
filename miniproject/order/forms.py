# order/forms.py
from django import forms
from .models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['name', 'phone', 'address', 'place', 'PIN', 'district', 'state']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street Address'}),
            'PIN': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'}),
            'place': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Place'}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'District'}),
        }



