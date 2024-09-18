from django import forms
from .models import BloodBank, DonationCamp, DonorRegistration,BloodDonation, DonorProfile, RecipientProfile

class BloodBankForm(forms.ModelForm):
    class Meta:
        model = BloodBank
        fields = ['name', 'address', 'contact_number', 'email', 'manager']

class DonationCampForm(forms.ModelForm):
    class Meta:
        model = DonationCamp
        fields = ['name', 'date', 'place']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'place': forms.TextInput(attrs={'class': 'form-control'}),
        }


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = DonorRegistration
        fields = ['user', 'camp']


class BloodDonationForm(forms.ModelForm):
    class Meta:
        model = BloodDonation
        fields = ['blood_group', 'donation_date']


class DonorProfileForm(forms.ModelForm):
    class Meta:
        model = DonorProfile
        fields = ['first_name', 'last_name', 'age', 'contact_number']

class RecipientProfileForm(forms.ModelForm):
    class Meta:
        model = RecipientProfile
        fields = ['first_name', 'last_name','age', 'contact_number']
