from django import forms
from .models import *


class CreateListingForm(forms.ModelForm):
    required_css_class = 'create-field'
    error_required_calss = 'error-field'
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': 'Auction Title',
                                                          'size':30}))
    price = forms.DecimalField(widget=forms.NumberInput(   attrs={'class': 'form-control',
                                                                  'placeholder': 'bit starting price',
                                                                   'size':30 }))
    image = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control',
                                                        'placeholder': 'Image URl',
                                                        'size':30,}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                               'rows': 15,
                                                               'columns':30}))
    class Meta:
        model = AuctionListing
        fields = ['name', 'price', 'image', 'description', 'category']
        


