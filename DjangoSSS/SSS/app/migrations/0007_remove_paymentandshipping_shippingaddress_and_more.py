# Generated by Django 5.0.4 on 2024-04-23 19:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_address_postcode_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentandshipping',
            name='shippingaddress',
        ),
        migrations.RemoveField(
            model_name='paymentandshipping',
            name='transaction_passed',
        ),
    ]
