
from django.urls import path
from .views import signupUser, loginUser, logoutUser, createProfile, account, delete_account, Home, editProfile

urlpatterns = [
    path('authenticate/login/',loginUser, name='login'),
    path('authenticate/logout/',logoutUser, name='logout'),
    path('authenticate/signup/',signupUser, name='signup'),
    path('authenticate/profile/',createProfile, name='createProfile'),
    path('authenticate/account/<str:username>/',account, name='account'),
    path('authenticate/deleteAccount/',delete_account, name='delete'),
    path('authenticate/editProfile/',editProfile, name='editProfile'),
    path('home/', Home, name='Home'),
]