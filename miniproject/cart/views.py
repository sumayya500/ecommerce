# from django.shortcuts import render,get_object_or_404, redirect 
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from product.models import Product
# from .models import Cart, CartItem
# from admindashboard.decorators import admin_restricted

# @admin_restricted
# @login_required(login_url='accounts:login_view')
# def add_to_cart(request, product_id):
    
#     if request.user.is_staff or request.user.is_superuser:
#         messages.error(request, "Admins cannot add items to the cart.")
#         return redirect('home')

#     product = get_object_or_404(Product, id=product_id)
#     cart, created = Cart.objects.get_or_create(user=request.user)
   
#     cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
#     if not item_created:
#         cart_item.quantity += 1  
#         cart_item.save()
    
#     messages.success(request, f"{product.name} has been added to your cart.")
#     return redirect('cart:cart_view')  

# @admin_restricted
# @login_required(login_url='accounts:login_view')
# def cart_view(request):
#     cart, created = Cart.objects.get_or_create(user=request.user)
#     items = CartItem.objects.filter(cart=cart)  # Fetch items from the cart
#     cart_items = CartItem.objects.filter(cart__user=request.user)
#     # Check if the cart is empty
#     if not items.exists():
#         messages.info(request, "Your cart is empty. Please add something.")
#         context = {
#             'items': [],
#             'total_price': 0,
#         }
#         return render(request, 'cart/cart.html', context)

#     for item in items:
#         # Ensure 'discount_percentage' is the field name in the Product model
#         if item.product.discount_percentage:
#             item.discount_price = item.product.price * (1 - item.product.discount_percentage / 100)
#         else:
#             item.discount_price = item.product.price
#         item.total_price = item.discount_price * item.quantity
#         item.save()

#     total_price = sum(item.total_price for item in items)

#     context = {
#         # 'items': items,
#         'cart_items': cart_items,
#         'total_price': total_price,  
#     }
#     return render(request, 'cart/cart.html', context)

# @admin_restricted
# def increase_quantity(request, cart_item_id):
#     cart_item = CartItem.objects.get(id=cart_item_id)
#     cart_item.quantity += 1
#     cart_item.save()
#     return redirect('cart_view')

# @admin_restricted
# def decrease_quantity(request, cart_item_id):
#     cart_item = CartItem.objects.get(id=cart_item_id)
#     if cart_item.quantity > 1:
#         cart_item.quantity -= 1
#         cart_item.save()
#     return redirect('cart_view')

# @admin_restricted
# def remove_from_cart(request, cart_item_id):
#     cart_item = CartItem.objects.get(id=cart_item_id)
#     cart_item.delete()
#     return redirect('cart_view')


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from product.models import Product
from .models import Cart, CartItem
from admindashboard.decorators import admin_restricted

@admin_restricted
@login_required(login_url='accounts:login_view')
def add_to_cart(request, product_id):
    if request.user.is_staff or request.user.is_superuser:
        messages.error(request, "Admins cannot add items to the cart.")
        return redirect('home')

    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.name} has been added to your cart.")
    return redirect('cart:cart_view')


@admin_restricted
@login_required(login_url='accounts:login_view')
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)

    total_price = 0
    for item in items:
        if item.product.discount_percentage:
            discount_price = item.product.price * (1 - item.product.discount_percentage / 100)
        else:
            discount_price = item.product.price
        item.total_price = discount_price * item.quantity
        total_price += item.total_price

    context = {
        'items': items,
        'total_price': total_price,
    }
    return render(request, 'cart/cart.html', context)


@admin_restricted
def increase_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart:cart_view')


@admin_restricted
def decrease_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_view')


@admin_restricted
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart:cart_view')
