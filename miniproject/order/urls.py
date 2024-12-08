from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    
    path('checkout/', views.checkout_view, name='checkout'),
    path('add_address/', views.add_address, name='add_address'),
    path('success/<int:order_id>/',views.success_view, name='success'),
    path('my_order/',views.my_order,name='my_order'),
    path('user_order_track/<int:order_id>/',views.user_order_track,name='user_order_track'),
    path('change-order-status/<int:pid>/', views.change_order_status, name="change_order_status"),
    path('order/<int:order_id>/request-return/', views.request_return, name='request_return'),

]


