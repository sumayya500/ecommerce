from django.urls import path
from product import views


app_name = 'product' 

urlpatterns = [
    path('',views.product,name="Product"),
    path('product/<int:product_id>/', views.product_detail_view, name='product_detail'),
    path('category_view/<str:category_name>/',views.category_view, name='category_view'),
    path('category_view/<str:category_name>/', views.category_view, name='category_view'), 
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),  # For adding products to the wishlist
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

]