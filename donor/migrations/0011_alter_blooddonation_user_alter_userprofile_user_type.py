# Generated by Django 5.1 on 2024-08-22 08:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0010_alter_blooddonation_user_alter_bloodrequest_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blooddonation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donor.userprofile'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_type',
            field=models.CharField(choices=[('donor', 'Donor'), ('recipient', 'Recipient'), ('admin', 'Admin')], max_length=10),
        ),
    ]
