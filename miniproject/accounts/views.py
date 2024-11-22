from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login,logout
from .models import CustomUser
from .forms import SignupForm
from django.contrib import messages
import random
from django.contrib.auth import authenticate,login as auth_login
from .forms import LoginForm  # Import your LoginForm
from product.models import *
from product.models import Product, Category
from .forms import ProfileUpdateForm
from django.contrib.auth.decorators import login_required



def index(request):
    products = Product.objects.all()
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
            return redirect('verify_otp')
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
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect('verify_otp')
    return render(request, 'accounts/verify_otp.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Attempt to authenticate the user
            user = authenticate(request, username=email, password=password)

            if user is not None:
                # Check if the user is staff
                if user.is_staff:
                    auth_login(request, user)  # Log the staff user in
                    messages.success(request, "Welcome back! You are now logged in as an admin.")
                    return redirect('admindashboard:admin_dashboard')  # Redirect to admin dashboard

                # For non-staff users, check email verification
                if user.email_verified:
                    auth_login(request, user)  # Log the regular user in
                    messages.success(request, "Welcome back! You are now logged in.")
                    return redirect('home')  # Redirect to home for regular users
                else:
                    messages.error(request, "Please verify your email before logging in.")
                    return redirect('login')  # Redirect back to login if email is not verified
            else:
                messages.error(request, "Invalid email or password. Please try again.")
                
    else:
        form = LoginForm()  # Create a new form instance if not a POST request

    return render(request, 'accounts/login.html', {'form': form})  # Ensure this template exists



 
def home_view(request):
    products = Product.objects.all()
    return render(request,'accounts/home.html',{'products':products})


def logout_view(request):
    return render(request,'accounts/index.html')


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

# @login_required
# def update_profile(request):
#     if request.method == 'POST':
#         form = ProfileUpdateForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')
#     else:
#         form = ProfileUpdateForm(instance=request.user)
#     return render(request, 'accounts/profileupdate.html', {'form': form})


