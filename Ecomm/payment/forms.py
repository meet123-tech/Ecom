from django import forms
from .models import ShippingAddress


class ShippingForm(forms.ModelForm): 

    shipping_full_name = forms.CharField(label="",  widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Full Name'}),required=True)
    shipping_email = forms.CharField(label="",  widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}), required=True)                                                                                
    shipping_address1 = forms.CharField(label="",  widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Address1'}), required=True)
    shipping_address2 = forms.CharField(label="",  widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Address2'}), required=False)
    shipping_city = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'City'}), required=True)
    shipping_state = forms.CharField(label="",  widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'State'}), required=False)
    shipping_postal_code = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Postal Code'}), required=False)
    shipping_country = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Country'}), required=True)

    

    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name','shipping_email', 'shipping_address1', 'shipping_address2',
                  'shipping_city', 'shipping_state', 'shipping_postal_code', 'shipping_country']
        exclude = ['user',]
 
class PaymentForm(forms.Form):

    card_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Card name'}), required=True)
    card_number = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Card number'}), required=True)
    expiry_month = forms.ChoiceField(label="", choices=[(i, i) for i in range(1, 13)], widget=forms.Select(attrs={'class': 'form-control'}))
    expiry_year = forms.ChoiceField(label="", choices=[(i, i) for i in range(2022, 2040)], widget=forms.Select(attrs={'class': 'form-control'}))
    cvv = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'CVV'}), required=True)
    



