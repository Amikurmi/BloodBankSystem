# Generated by Django 5.1 on 2024-08-22 10:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0012_alter_donorregistration_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blooddonation',
            name='blood_group',
            field=models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], max_length=10),
        ),
        migrations.AlterField(
            model_name='blooddonation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donor.donorprofile'),
        ),
        migrations.AlterField(
            model_name='donationcamp',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='donationcamp',
            name='organizer_contact',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='donationcamp',
            name='place',
            field=models.CharField(max_length=200),
        ),
    ]
