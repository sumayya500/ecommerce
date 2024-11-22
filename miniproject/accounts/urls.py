# # accounts/urls.py
from django.urls import path
from accounts import views
from .views import signup_view, verify_otp_view, login_view



urlpatterns = [
    path('', views.index, name='index'),  # Index view for accounts
    path('accounts/signup/', signup_view, name='signup'),  # Signup view
    path('verify_otp/', verify_otp_view, name='verify_otp'),  # OTP verification view
    path('accounts/login/', login_view, name='login'),  # Login view
    path('home/', views.home_view, name='home'),  # Home view
    path('logout/',views.logout_view,name='logout'),
    path('profile/', views.profile_view, name='profile'),
    # path('profile/update/', views.update_profile, name='update_profile'),
]
