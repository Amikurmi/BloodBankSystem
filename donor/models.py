from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class UserProfile(models.Model):
    USER_TYPES = (
        ('donor', 'Donor'),
        ('recipient', 'Recipient'),
        ('admin', 'Admin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)

    def __str__(self):
        return self.user.username


class DonorProfile(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField()
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user.user.username})"

class DonationCamp(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    place = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class BloodDonation(models.Model):
    BLOOD_GROUP_CHOICES = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    )

    user = models.ForeignKey(DonorProfile, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    donation_date = models.DateField()
    status = models.CharField(max_length=10, default='Pending')

    def __str__(self):
        return f'{self.user.user.username} - {self.blood_group}'



class RecipientProfile(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField()
    contact_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user.user.username})"


class BloodRequest(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    required_date = models.DateField()
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=10, default='Pending')

    def __str__(self):
        return f'{self.user.user.username} - {self.blood_group} - {self.required_date}'


class BloodBank(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class DonorRegistration(models.Model):
    user = models.ForeignKey(DonorProfile, on_delete=models.CASCADE)
    camp = models.ForeignKey(DonationCamp, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.user.username} - {self.camp.name}"
    
class Certificate(models.Model):
    donation = models.OneToOneField(BloodDonation, on_delete=models.CASCADE)
    certificate_file = models.FileField(upload_to='certificates/')

    def __str__(self):
        return f"Certificate for {self.donation.donor}"