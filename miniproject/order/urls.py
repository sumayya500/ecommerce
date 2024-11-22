from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    
    path('checkout/', views.checkout_view, name='checkout'),
    path('add_address/', views.add_address, name='add_address'),
    # path('place_order/', views.place_order, name='place_order'),
    # path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
   
]
