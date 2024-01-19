
from django.urls import path
from .views import register_vendor, login_vendor, logoutVendor, createProfile_vendor, Vendor_account,delete_Vendoraccount, editVendor_Profile, Dashboard, list_product,get_by_category, get_listing_detail, get_all_listingsby_vendor,get_all_recent_listings_vendor,vendor_create_deal_AmountOff,vendor_create_deal_Buy_Get ,get_product_pk_for_deal, get_all_deals,get_type_of_discount

urlpatterns = [
    path('vendor/Register/hereasVendor/',register_vendor, name='register_as_vendor'),
    path('vendor/Login/hereasVendor/',login_vendor, name='login_vendor'),
    path('vendor/Logout/hereasVendor/',logoutVendor, name='logout_vendor'),
    path('vendor/CreateProfile/hereasVendor/',createProfile_vendor, name='createProfile_vendor'),
    path('vendor/YourAccount/hereasVendor/<str:username>/',Vendor_account, name='Vendor_account'),
    path('vendor/hereasVendor/deleteAccount/',delete_Vendoraccount, name='delete_Vendoraccount'),
    path('vendor/EditProfile/hereasVendor/',editVendor_Profile, name='editVendor_Profile'),
    path('vendor/YourDashboard/hereasVendor/<str:username>/', Dashboard, name='Dashboard'),
    path('list_product/<str:username>/', list_product, name='list_product'),
    path('products/category/<str:product_category>/<str:username>/', get_by_category, name='get_by_category'),
    path('products/Listing_detail/<int:pk>/', get_listing_detail, name='get_listing_detail'),
    path('products/all_by_vendor/<str:username>/', get_all_listingsby_vendor, name='get_all_listingsby_vendor'),
    path('products/recent_products/<str:username>/', get_all_recent_listings_vendor, name='get_all_recent_listings_vendor'),
    path('products/create_product_deals_AmountOff/<str:username>/<int:pk>/', vendor_create_deal_AmountOff, name='vendor_create_deal_AmountOff'),
    path('products/create_product_deals_Buy_get_one/<str:username>/<int:pk>/', vendor_create_deal_Buy_Get, name='vendor_create_deal_Buy_Get'),
    path('products/get_product_for_deals/<str:username>/', get_product_pk_for_deal, name='get_product_pk_for_deal'),
    path('products/get_discount_type_for_deals/<int:pk>/<str:username>/', get_type_of_discount, name='get_type_of_discount'),
    path('products/get_all_deals/<str:username>/', get_all_deals, name='get_all_deals'),
]