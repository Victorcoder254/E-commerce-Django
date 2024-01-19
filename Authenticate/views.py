from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from .models import UserProfile

def signupUser(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        newuser= User.objects.create_user(username=username, password=password, email=email)

        newuser.first_name=firstname
        newuser.last_name=lastname

        newuser.save()

        return redirect('login')
    return render(request, 'authenticate/signup.html')

def createProfile(request):
    logged_in_user = request.user
    if request.method == 'POST':
        profile_image = request.FILES.get('profile_image')

        if logged_in_user.is_authenticated:
            userprofile = UserProfile.objects.create(user=logged_in_user, profile_image=profile_image) 
            userprofile.profile_image = profile_image

            userprofile.save()

        return redirect('Home')

    # If the request method is not POST, it means it's a GET request
    try:
        # Try to get the user's profile
        userprofile = UserProfile.objects.get(user=logged_in_user)
    except UserProfile.DoesNotExist:
        # If the user doesn't have a profile, set userprofile to None
        userprofile = None
    return render(request, 'authenticate/profile.html', {'userprofile':userprofile})

def editProfile(request):

    logged_in_user = request.user

    if request.method == 'POST':
        profile_image = request.FILES.get('profile_image')
        if logged_in_user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=logged_in_user)
                # Update the profile fields
                profile.profile_image = profile_image or profile.profile_image
                profile.save()
            except UserProfile.DoesNotExist:
                # Handle the case where the profile does not exist for the user
                return redirect('login')
        return redirect('account', username=request.user.username) 
    try:
        # Try to get the user's profile
        userprofile = UserProfile.objects.get(user=logged_in_user)
    except UserProfile.DoesNotExist:
        # If the user doesn't have a profile, set userprofile to None
        userprofile = None
    return render(request, 'authenticate/editProfile.html', {'userprofile':userprofile})


@login_required
def account(request, username):
    try:
       user = User.objects.get(username=username)
       userprofile = UserProfile.objects.get(user=user)
    except User.DoesNotExist:
       return render(request, 'authenticate/404.html')
    except UserProfile.DoesNotExist:
       return render(request, 'authenticate/404.html')
    return render(request, 'authenticate/account.html', {'userprofile':userprofile})



def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

            try:
                profile = UserProfile.objects.get(user=user)
                return redirect('Home')
            except UserProfile.DoesNotExist:
                return redirect('createProfile')
            
        else:
            return redirect('login')   
    return render(request, 'authenticate/login.html')

def logoutUser(request):
    logout(request)
    return redirect('Home')


@login_required
def delete_account(request):
    if request.method == 'GET':
        user = request.user
        user.delete()
        logout(request)  # Log the user out after deleting their account
        return redirect('Home') 

def Home(request):
    return render(request, 'authenticate/home.html')

    
