from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login,logout
from .models import CustomUser
from .forms import SignupForm
from django.contrib import messages
import random
from django.contrib.auth import authenticate,login as auth_login
from .forms import LoginForm 
from product.models import *
from product.models import Product, Category
from .forms import ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import EditProfileForm 
from django.contrib.auth.forms import PasswordChangeForm
import string
from django.contrib.auth import get_user_model

def index(request):
    products = Product.objects.all()[:6]
    context = {'products': products}
    return render(request,'accounts/index.html',context)
 
def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(user_email, otp):
    subject = 'Your OTP Verification Code'
    message = f'Your OTP verification code is {otp}. Please enter this code to verify your email.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, email_from, recipient_list)


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if CustomUser.objects.filter(email=email, email_verified=True).exists():
                messages.error(request, "Email is already registered.")
                return redirect('signup')

            otp = generate_otp()
            user = CustomUser(
                username=form.cleaned_data['username'],
                email=email,
                phone_number=form.cleaned_data['phone_number'],
                otp=otp,
                is_active=False  # Deactivate until email verification
            )
            user.set_password(form.cleaned_data['password1'])
            user.save()
            
            send_otp_email(user.email, otp)
            request.session['user_id'] = user.id
            messages.success(request, "OTP sent to your email. Please verify.")
            return redirect('accounts:verify_otp')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form}) 


def verify_otp_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('signup')

    user = CustomUser.objects.get(id=user_id)
    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        if otp_input == user.otp:
            user.email_verified = True
            user.is_active = True  # Activate account after verification
            user.otp = ''  # Clear OTP after successful verification
            user.save()
            login(request, user)
            messages.success(request, "Email verified! You are now logged in.")
            return redirect('accounts:login')
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect('accounts:verify_otp')
    return render(request, 'accounts/verify_otp.html')

# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']

#             # Attempt to authenticate the user
#             user = authenticate(request, username=email, password=password)

#             if user is not None:
#                 # Check if the user is staff
#                 if user.is_staff:
#                     auth_login(request, user)  # Log the staff user in
#                     messages.success(request, "Welcome back! You are now logged in as an admin.")
#                     return redirect('admindashboard:admin_dashboard')  # Redirect to admin dashboard 
#                 if user.email_verified:
#                     auth_login(request, user)  # Log the regular user in
#                     messages.success(request, "Welcome back! You are now logged in.")
#                     return redirect('accounts:home')  # Redirect to home for regular users
#                 else:
#                     messages.error(request, "Please verify your email before logging in.")
#                     return redirect('accounts:login')  # Redirect back to login if email is not verified
#             else:
#                 messages.error(request, "Invalid email or password. Please try again.")
                
#     else:
#         form = LoginForm()  # Create a new form instance if not a POST request

      
#     return render(request, 'accounts/login.html', {'form': form})  # Ensure this template exists


def login_view(request):
    # Clear any session or user data that may have been carried over from previous logins
    if 'email' in request.session:
        del request.session['email']
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Attempt to authenticate the user
            user = authenticate(request, username=email, password=password)

            if user is not None:
                if user.is_staff:
                    auth_login(request, user)
                    messages.success(request, f"Welcome back, {user.first_name}! You are now logged in as an admin.")
                    return redirect('admindashboard:admin_dashboard')
                if user.email_verified:
                    auth_login(request, user)
                    messages.success(request, f"Welcome back, {user.first_name}!")
                    return redirect('accounts:home')
                else:
                    messages.error(request, "Please verify your email before logging in.")
                    return redirect('accounts:login')
            else:
                messages.error(request, "Invalid email or password. Please try again.")
    else:
        form = LoginForm()  # Create a new form instance if not a POST request

    return render(request, 'accounts/login.html', {'form': form})

@login_required
def home_view(request):
    products = Product.objects.all()[:6]  # Fetch all products

    for product in products:
        if product.discount_percentage:
            product.discount_price = product.price * (1 - product.discount_percentage / 100)
        else:
            product.discount_price = product.price

    context = {
        'products': products,
    }
    return render(request, 'accounts/home.html', context)

    

@login_required
def logout_view(request):
    return render(request,'accounts/login.html')


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('accounts:profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Update the session to keep the user logged in
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password has been changed successfully.')
            return redirect('accounts:profile')  # Redirect to the profile page after successful password change
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'accounts/change_password.html', {'form': form})


# accounts/views.py
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
  # Assuming you have a utils.py file with generate_otp function

User = get_user_model()

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            otp = generate_otp()
            user.otp = otp
            user.save()
            send_mail(
                'Your OTP for password reset',
                f'Your OTP is {otp}.',
                'your_email@example.com',
                [email],
                fail_silently=False,
            )
            return redirect('accounts:reset_password')
        except User.DoesNotExist:
            return render(request, 'accounts/forgot_password.html', {'error': 'Email not found.'})
    return render(request, 'accounts/forgot_password.html')

# accounts/views.py
def reset_password(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        new_password = request.POST['new_password']
        try:
            user = User.objects.get(otp=otp)
            user.set_password(new_password)
            user.otp = ''  # Clear the OTP field
            user.save()
            return redirect('accounts:login')
        except User.DoesNotExist:
            return render(request, 'accounts/reset_password.html', {'error': 'Invalid OTP.'})
    return render(request, 'accounts/reset_password.html')

def wallet(request):
    user = request.user

    wallet = user.wallet
    return render(request,'accounts/wallet.html',{'wallet':wallet})