from django.db import models
from django.contrib.auth.models import User

class VendorProfile(models.Model):
    vendor = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.TextField(blank=True, null=True)
    contact_info = models.TextField(blank=True, null=True)
    business_logo = models.ImageField(upload_to='business_logo/', blank=True, null=True)
    business_address = models.TextField(blank=True, null=True)
    business_permit = models.FileField(upload_to='business_permit/', blank=True, null=True)

class Vendors_product(models.Model):
    ACCESSORIES = 'ACCESSORIES'
    CLOTHES = 'clothes'
    SHOES = 'shoes'
    JEWELRY = 'jewelry'
    HANDBAGS = 'handbags'
    FANCY = 'fancy'
    FRAGRANCE = 'fragnance'

    BEAUTY_PRODUCTS = 'BEAUTY_PRODUCTS'
    SKINCARE = 'skincare'
    MAKEUP = 'makeup'
    HAIRCARE = 'haircare'
    NAILCARE = 'nailcare'

    PRODUCT_CATEGORY = [
        (ACCESSORIES, [
            (CLOTHES, 'Clothes'),
            (SHOES, 'Shoes'),
            (JEWELRY, 'Jewelry'),
            (HANDBAGS, 'Handbags'),
            (FANCY, 'Fancy'),
            (FRAGRANCE, 'Fragnance'),
        ]),
        (BEAUTY_PRODUCTS, [
            (SKINCARE, 'Skincare'),
            (MAKEUP, 'Makeup'),
            (HAIRCARE, 'Haircare'),
            (NAILCARE, 'Nailcare'),
        ]),
    ]


    vendoruser = models.ForeignKey(User, on_delete=models.CASCADE) 
    cover_image = models.ImageField(upload_to='product_cover_image/', blank=True, null=True)
    product_name = models.CharField(max_length=50, blank=True, null=True)
    available_size = models.CharField(max_length=50, blank=True, null=True)
    price = models.CharField(max_length=50, blank=True, null=True)
    in_stock = models.BooleanField(default = True, null = True, blank=True)
    description = models.TextField(blank=True, null = True)
    product_details = models.TextField(blank=True, null = True)
    product_detail_image_1 = models.ImageField(upload_to='product_detail_image/', blank=True, null=True)
    product_detail_image_2 = models.ImageField(upload_to='product_detail_image/', blank=True, null=True)
    product_detail_image_3 = models.ImageField(upload_to='product_detail_image/', blank=True, null=True)
    product_detail_image_4 = models.ImageField(upload_to='product_detail_image/', blank=True, null=True)
    product_detail_image_5 = models.ImageField(upload_to='product_detail_image/', blank=True, null=True)
    product_image_color_1 = models.ImageField(upload_to='product_image_color/', blank=True, null=True)
    product_image_color_2 = models.ImageField(upload_to='product_image_color/', blank=True, null=True)
    product_image_color_3 = models.ImageField(upload_to='product_image_color/', blank=True, null=True)
    product_image_color_4 = models.ImageField(upload_to='product_image_color/', blank=True, null=True)
    product_sizechart_image = models.ImageField(upload_to='product_sizeChart/', blank=True, null=True)
    product_category = models.CharField(choices = PRODUCT_CATEGORY, max_length=50, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True,  blank=True, null=True)

    class Meta:
        ordering = ['-date_added']



class vendors_orders_discount(models.Model):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Vendors_product, on_delete=models.CASCADE)  # Use quotes to avoid reference issues
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    discounted_price = models.CharField(max_length=50, blank=True, null=True)
    name_buy_get_one = models.TextField(blank=True, null=True)
    image_buy_get_one = models.ImageField(upload_to='buy_one_get/',blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)


    def percentage_discount(self):
        try:
            previous_price = float(self.product.price)
            discounted_price = float(self.discounted_price)

            if previous_price > 0:
                percentage_off = ((previous_price - discounted_price) / previous_price) * 100
                return round(percentage_off, 2)
        except (ValueError, TypeError):
            # Handle the case where conversion to float fails
            pass

        return 0   

    class Meta:
        ordering = ['-start_date']
 



