from django import forms

from .models import FoodClaim, FoodListing


class DateTimeLocalInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class FoodListingForm(forms.ModelForm):
    class Meta:
        model = FoodListing
        fields = [
            'title',
            'description',
            'quantity',
            'pickup_location',
            'latitude',
            'longitude',
            'expiry_date',
        ]
        widgets = {
            'expiry_date': DateTimeLocalInput(),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['expiry_date'].input_formats = ['%Y-%m-%dT%H:%M']


class FoodClaimForm(forms.ModelForm):
    class Meta:
        model = FoodClaim
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
        }
