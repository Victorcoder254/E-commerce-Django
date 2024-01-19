from django.contrib import admin
from .models import*

models = [VendorProfile, Vendors_product, vendors_orders_discount]
admin.site.register(models)
