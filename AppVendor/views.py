from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import VendorProfile, Vendors_product, vendors_orders_discount
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.urls import reverse
from django.db import IntegrityError

def register_vendor(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        new_vendor = User.objects.create_user(username=username, email=email, password=password)

        new_vendor.first_name=firstname
        new_vendor.last_name=lastname
        vendor_group, created = Group.objects.get_or_create(name='vendors')
        new_vendor.groups.add(vendor_group)

        new_vendor.save()

        return redirect('login_vendor')
    return render(request, 'vendor/signup.html')



def login_vendor(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

            if hasattr(user, 'vendorprofile'):
                return redirect(reverse('dashboard', args=[request.user.username]))
            else:
                return redirect('createProfile_vendor')

        else:
            return redirect('login_vendor')

    return render(request, 'vendor/login.html')


def createProfile_vendor(request):
    logged_in_vendor = request.user
    if request.method == 'POST':
        business_name = request.POST.get('business_name')
        contact_info = request.POST.get('contact_info')
        business_address = request.POST.get('business_address')
        business_logo = request.FILES.get('business_logo')
        business_permit = request.FILES.get('business_permit')

        if logged_in_vendor.is_authenticated:
            try:
                # Check if a VendorProfile already exists for the vendor
                vendorprofile = VendorProfile.objects.get(vendor=logged_in_vendor)
                
                # Update the existing profile
                vendorprofile.business_name = business_name
                vendorprofile.contact_info = contact_info
                vendorprofile.business_address = business_address
                vendorprofile.business_logo = business_logo
                vendorprofile.business_permit = business_permit
                vendorprofile.save()
                
            except VendorProfile.DoesNotExist:
                # If no profile exists, create a new one
                vendorprofile = VendorProfile.objects.create(
                    vendor=logged_in_vendor,
                    business_name=business_name,
                    contact_info=contact_info,
                    business_address=business_address,
                    business_logo=business_logo,
                    business_permit=business_permit,
                )
                
            except IntegrityError as e:
                # Handle any other IntegrityError (e.g., database constraint violations)
                print(e)
                return HttpResponse("An error occurred while processing your request.")
                
        return redirect('Dashboard', username=logged_in_vendor.username)
    
    return render(request, 'vendor/vendorProfile.html')

def editVendor_Profile(request):

    logged_in_vendor = request.user

    if request.method == 'POST':
        business_name = request.POST.get('business_name')
        contact_info = request.POST.get('contact_info')
        business_address = request.POST.get('business_address')
        business_logo = request.FILES.get('business_logo')
        business_permit = request.FILES.get('business_permit')

        if logged_in_vendor.is_authenticated:
            try:
                vendorprofile = VendorProfile.objects.get(vendor=logged_in_vendor)
                # Update the profile fields
                vendorprofile.business_name = business_name or vendorprofile.business_name
                vendorprofile.contact_info = contact_info or vendorprofile.contact_info
                vendorprofile.business_address = business_address or vendorprofile.business_address
                vendorprofile.business_logo = business_logo or vendorprofile.business_logo
                vendorprofile.business_permit = business_permit or vendorprofile.business_permit
                vendorprofile.save()
            except VendorProfile.DoesNotExist:
                # Handle the case where the profile does not exist for the user
                return redirect('login_vendor')
        return redirect('account_vendor', username=request.user.username) 
    try:
        # Try to get the user's profile
        vendorprofile = VendorProfile.objects.get(vendor=logged_in_vendor)
    except VendorProfile.DoesNotExist:
        # If the user doesn't have a profile, set userprofile to None
        vendorprofile = None
    return render(request, 'vendor/editVendor_profile.html', {'vendorprofile':vendorprofile})

@login_required
def Vendor_account(request, username):
    try:
       user = User.objects.get(username=username)
       vendorprofile = VendorProfile.objects.get(vendor=user)
    except User.DoesNotExist:
       return render(request, 'vendor/404.html')
    except VendorProfile.DoesNotExist:
       return render(request, 'vendor/404.html')
    return render(request, 'vendor/account_vendor.html', {'vendorprofile':vendorprofile})


def logoutVendor(request):
    logout(request)
    return redirect('login_vendor')


@login_required
def delete_Vendoraccount(request):
    if request.method == 'GET':
        user = request.user
        user.delete()
        logout(request)  # Log the user out after deleting their account
        return redirect('login_vendor') 

@login_required
def Dashboard(request, username):
    vendor = request.user
    products = Vendors_product.objects.filter(vendoruser=vendor)[:4]
    return render(request, 'vendor/Dashboard.html', {'products':products})

def list_product(request, username):
    if request.method == 'POST':

        vendor = request.user
        cover_image = request.FILES.get('cover_image')
        product_name = request.POST.get('product_name')
        price = request.POST.get('price')
        instock = request.POST.get('instock', False)== 'on'
        description = request.POST.get('description')
        product_details = request.POST.get('product_details')
        product_detail_image_1 = request.FILES.get('product_detail_image_1')
        product_detail_image_2 = request.FILES.get('product_detail_image_2')
        product_detail_image_3 = request.FILES.get('product_detail_image_3')
        product_detail_image_4 = request.FILES.get('product_detail_image_4')
        product_detail_image_5 = request.FILES.get('product_detail_image_5')
        product_image_color_1 = request.FILES.get('product_image_color_1')
        product_image_color_2 = request.FILES.get('product_image_color_2')
        product_image_color_3 = request.FILES.get('product_image_color_3')
        product_image_color_4 = request.FILES.get('product_image_color_4')
        product_sizechart_image = request.FILES.get('product_sizechart_image')
        product_category = request.POST.get('product_category')

        new_product = Vendors_product.objects.create(vendoruser=vendor, 
                                                     cover_image=cover_image, 
                                                     product_name=product_name,
                                                     price=price,
                                                     in_stock=instock, 
                                                     description=description,
                                                     product_details=product_details,
                                                     product_detail_image_1=product_detail_image_1,
                                                     product_detail_image_2=product_detail_image_2,
                                                     product_detail_image_3=product_detail_image_3,
                                                     product_detail_image_4=product_detail_image_4,
                                                     product_detail_image_5=product_detail_image_5,
                                                     product_image_color_1=product_image_color_1,
                                                     product_image_color_2=product_image_color_2,
                                                     product_image_color_3=product_image_color_3,
                                                     product_image_color_4=product_image_color_4,
                                                     product_sizechart_image=product_sizechart_image,
                                                     product_category=product_category,
                                                     )
        new_product.save()
        
        return redirect('Dashboard', username=request.user.username)
    
    product_categories = Vendors_product.PRODUCT_CATEGORY

    return render(request, 'vendor/list_product.html', {'product_categories': product_categories})



def get_by_category(request, product_category, username):
    vendor = request.user
    products = Vendors_product.objects.filter(product_category=product_category, vendoruser=vendor)
    return render(request, 'vendor/category.html', {'products': products, 'category': product_category})

def get_listing_detail(request, pk):
    product = Vendors_product.objects.get(pk=pk)
    return render(request, 'vendor/detail_listing.html', {'product':product})


def get_all_listingsby_vendor(request, username):
    vendor = request.user
    products = Vendors_product.objects.filter(vendoruser=vendor)
    return render(request, 'vendor/all_listings.html', {'products':products})


def get_all_recent_listings_vendor(request, username):
    vendor = request.user
    products = Vendors_product.objects.filter(vendoruser=vendor)[:5]
    return render(request, 'vendor/recent_listings.html', {'products':products})


def get_product_pk_for_deal(request, username):
    vendor=request.user
    products = Vendors_product.objects.filter(vendoruser=vendor)

    return render(request, 'vendor/Products_For_deal.html', {'products':products})


def get_type_of_discount(request, username, pk):
    vendor=request.user
    product = Vendors_product.objects.get(pk=pk)
    return render(request, 'vendor/Discount_Type.html', {'product':product})

def vendor_create_deal_AmountOff(request, pk, username):
    logged_in_vendor=request.user
    product = Vendors_product.objects.get(pk=pk)

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        discounted_price = request.POST.get('discounted_price', '0')
        name_buy_get_one = request.POST.get('name_buy_get_one', 'name')
        image_buy_get_one = request.FILES.get('image_buy_get_one', 'pexels-karolina-grabowska-5625042.jpg')

        new_vendor_deal = vendors_orders_discount.objects.create(vendor=logged_in_vendor,
                                              product=product,
                                              start_date=start_date,
                                              end_date=end_date,
                                              discounted_price=discounted_price,
                                              name_buy_get_one=name_buy_get_one,
                                              image_buy_get_one=image_buy_get_one,
                                              )


        new_vendor_deal.save()

        return redirect('Dashboard', username=request.user.username)
    return render(request, 'vendor/List_deal_amountOFF.html')


def vendor_create_deal_Buy_Get(request, pk, username):
    logged_in_vendor=request.user
    product = Vendors_product.objects.get(pk=pk)

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        discounted_price = request.POST.get('discounted_price', '0')
        name_buy_get_one = request.POST.get('name_buy_get_one', 'name')
        image_buy_get_one = request.FILES.get('image_buy_get_one', 'pexels-karolina-grabowska-5625042.jpg')

        new_vendor_deal = vendors_orders_discount.objects.create(vendor=logged_in_vendor,
                                              product=product,
                                              start_date=start_date,
                                              end_date=end_date,
                                              discounted_price=discounted_price,
                                              name_buy_get_one=name_buy_get_one,
                                              image_buy_get_one=image_buy_get_one,
                                              )


        new_vendor_deal.save()

        return redirect('Dashboard', username=request.user.username)
    return render(request, 'vendor/List_deal_Buy_get.html')

def get_all_deals(request, username):
    logged_in_vendor = request.user
    deals = vendors_orders_discount.objects.filter(vendor=logged_in_vendor)
    return render(request, 'vendor/All_Deals.html', {'deals':deals})
