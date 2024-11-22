from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, Address
from .forms import AddressForm


@login_required
def checkout_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()

    for item in items:
        if item.product.discount_percentage:
            item.discount_price = item.product.price * (1 - item.product.discount_percentage / 100)
        else:
            item.discount_price = item.product.price
        item.total_price = item.discount_price * item.quantity

    total_price = sum(item.total_price for item in items)

    user_addresses = Address.objects.filter(user=request.user).order_by('-id')[:3]
    selected_address = None

    if request.method == "POST":
        address_id = request.POST.get("selected_address")
        selected_address = Address.objects.filter(id=address_id, user=request.user).first()

        if selected_address:
            # Proceed to payment process
            return redirect('process_payment')  # Replace 'process_payment' with your payment URL name

    context = {
        'items': items,
        'total_price': total_price,
        'addresses': user_addresses,
        'selected_address': selected_address,
    }
    return render(request, 'order/checkout.html', context)



@login_required
def add_address(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            return redirect('checkout')  # Redirect back to checkout page
    else:
        form = AddressForm()

    context = {
        'form': form,
    }
    return render(request, 'order/addaddress.html', context)

