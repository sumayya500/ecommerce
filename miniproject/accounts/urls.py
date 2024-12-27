# # accounts/urls.py
from django.urls import path
from accounts import views
from .views import signup_view, verify_otp_view, login_view

app_name = 'accounts'

urlpatterns = [
    # path('', views.login_view, name='login'), 
    path('', views.index, name='index'), # Index view for accounts
    path('accounts/signup/', signup_view, name='signup'),  # Signup view
    path('verify_otp/', verify_otp_view, name='verify_otp'),  # OTP verification view
    path('login/', login_view, name='login'),  # Login view
    path('home/', views.home_view, name='home'),  # Home view
    path('logout/',views.logout_view,name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('password/change/', views.change_password_view, name='change_password'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('wallet/',views.wallet,name='wallet'),
   

]
