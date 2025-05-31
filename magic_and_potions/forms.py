from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()

class UserSignupForm(UserCreationForm):

    first_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={

        'placeholder': 'First Name',
        'class': 'long-input',

    }))

    last_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={

        'placeholder': 'Last Name',
        'class': 'long-input',

    }))

    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={

        'placeholder': 'Email',
        'class': 'long-input',

    }))

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={

        'placeholder': 'Password',
        'class': 'long-input',

    }))

    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={

        'placeholder': 'Confirm Password',
        'class': 'long-input',

    }))

    class Meta:

        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']


class DeliveryAddressForm(forms.ModelForm):

    address = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={

        'placeholder': 'Address',
        'class': 'long-input',

    }))
    
    address_2 = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={

        'placeholder': 'Address 2 (Optional)',
        'class': 'long-input',

    }))
    
    region = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={

        'placeholder': 'County/Region',
        'class': 'long-input',

    }))
    
    postcode = forms.CharField(max_length=10, required=True, widget=forms.TextInput(attrs={

        'placeholder': 'Postcode',
        'class': 'long-input',

    }))
    
    class Meta:

        model = DeliveryAddress
        fields = ['address', 'address_2', 'region', 'postcode']



class PaymentDetailForm(forms.ModelForm):

    accountnumber = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={

        'placeholder': 'Card Number: 1234 1234 1234 1234',
        'class': 'long-input',

    }))
    
    expiration_date = forms.CharField(max_length=5, required=True, widget=forms.TextInput(attrs={

        'placeholder': 'Exp Date: MM/YY',
        'class': 'long-input',

    }))
    
    cvc = forms.CharField(max_length=3, required=True, widget=forms.TextInput(attrs={

        'placeholder': 'CVC: 123',
        'class': 'long-input',

    }))
    
    class Meta:
        
        model = PaymentDetail
        fields = ['accountnumber', 'expiration_date', 'cvc']

