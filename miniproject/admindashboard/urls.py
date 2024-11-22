from django.urls import path
from . import views 

app_name = 'admindashboard'

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user_management/', views.user_management, name='user_management'),
    path('activate-user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('deactivate-user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
    path('logout/', views.logout_view, name='logout'),
    path('productdashboard/',views.product_dashboard,name='product_dashboard'),
    path('productdashboard/add/', views.add_product, name='add_product'),
    path('productdashboard/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('productdashboard/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),
]


