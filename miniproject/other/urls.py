from django.urls import path
from . import views

app_name = 'other'

urlpatterns = [
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('shop/', views.shop, name='shop'),
    path('product_search/', views.product_search, name='product_search'),
    path('product/category_view/<path:category_name>/', views.filter_by_category, name='category_view'),


]