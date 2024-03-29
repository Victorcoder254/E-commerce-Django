# Generated by Django 5.0.1 on 2024-01-19 07:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppVendor', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='vendors_product',
            name='product_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='vendors_orders_discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('discounted_price', models.CharField(blank=True, max_length=50, null=True)),
                ('name_buy_get_one', models.TextField(blank=True, null=True)),
                ('image_buy_get_one', models.ImageField(blank=True, null=True, upload_to='buy_one_get/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AppVendor.vendors_product')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-start_date'],
            },
        ),
        migrations.DeleteModel(
            name='vendors_orders_discounts',
        ),
    ]
