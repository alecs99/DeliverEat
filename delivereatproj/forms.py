from django import forms
from delivereatproj import models


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=10)
    last_name = forms.CharField(max_length=10)
    e_mail = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=10)
    address = forms.Textarea()

    class Meta:
        model = models.UserProfile
        exclude = ['user']
