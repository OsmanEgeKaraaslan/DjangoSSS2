# Generated by Django 5.0.4 on 2024-04-23 20:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_remove_paymentandshipping_shippingaddress_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentandShipping2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=2)),
                ('postcode', models.CharField(max_length=100)),
                ('cardNumber', models.BigIntegerField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.customer')),
                ('items_bought', models.ManyToManyField(to='app.cartitem')),
            ],
        ),
        migrations.DeleteModel(
            name='PaymentandShipping',
        ),
    ]
