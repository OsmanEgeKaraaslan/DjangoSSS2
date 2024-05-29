
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PaymentandShipping2

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
class CheckoutForm(forms.ModelForm):
    class Meta:
        model = PaymentandShipping2
        fields = ['street', 'city', 'state', 'postcode', 'cardNumber']