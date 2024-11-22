from django.shortcuts import render,get_object_or_404, redirect 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from product.models import Product
from .models import Cart, CartItem

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
   
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += 1  
        cart_item.save()
    
    messages.success(request, f"{product.name} has been added to your cart.")
    return redirect('cart_view')  




@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    # total_price = sum(item.product.price * item.quantity for item in items)
    for item in items:
        # Ensure 'discount_percentage' is the field name in the Product model
        if item.product.discount_percentage:
            item.discount_price = item.product.price * (1 - item.product.discount_percentage / 100)
        else:
            item.discount_price = item.product.price
        item.total_price = item.discount_price * item.quantity

    total_price = sum(item.total_price for item in items)

    
    context = {
        'items': items,
        'total_price': total_price,
    }
    return render(request, 'cart/cart.html', context)


def increase_quantity(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_view')

def decrease_quantity(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('cart_view')

def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.delete()
    return redirect('cart_view')


