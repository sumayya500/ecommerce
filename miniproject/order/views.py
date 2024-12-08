from django.shortcuts import redirect, render, get_object_or_404
from .forms import AddressForm
from product. models import Product
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from .models import Orders, Cart, Address, Payments, CartItem
from django.contrib.auth.models import User
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)  # Fetch items from the cart

    # Check if the cart is empty
    if not items.exists():
        messages.error(request, "Your cart is empty. Please add products to proceed to checkout.")
        return redirect('accounts:home')  # Redirect to your product list or another relevant page

    # Calculate discounted price and total price
    for item in items:
        if item.product.discount_percentage:
            item.discount_price = item.product.price * (1 - item.product.discount_percentage / 100)
        else:
            item.discount_price = item.product.price
        item.total_price = item.discount_price * item.quantity
        item.save()

    total_price = sum(item.total_price for item in items)

    user_addresses = Address.objects.filter(user=request.user).order_by('-id')[:3]
    selected_address = None

    if request.method == "POST":
        address_id = request.POST.get("address_id")
        payment_method = request.POST.get("payment_method")
        selected_address = Address.objects.filter(id=address_id, user=request.user).first()

        if selected_address and payment_method:
            # Create the order
            order = Orders.objects.create(
                user=request.user,
                address=selected_address,
                total=total_price,
                payment_method=payment_method,
                is_paid=False,
                cart=cart
            )
            for item in items:
                order.items.add(item)
            order.save()

            # Handle payment for Cash on Delivery
            if payment_method == 'COD':
                Payments.objects.create(
                    order=order,
                    total_amount=total_price,
                    payment_status='Payment_Succeeded',  # Mark as succeeded since it's COD
                )
                items.delete()
                messages.success(request, "Your order was successfully placed! Please add products to your cart for future purchases.")
                return redirect('order:success', order_id=order.id)

            # Handle payment for Stripe
            elif payment_method == 'STRIPE':
                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': 'Total Order',
                            },
                            'unit_amount': int(total_price * 100),
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    success_url=request.build_absolute_uri(reverse('order:success', args=[order.id])) + "?session_id={CHECKOUT_SESSION_ID}",
                    cancel_url=request.build_absolute_uri(reverse('order:checkout')),
                )

                # Save payment details in the Payments model
                Payments.objects.create(
                    order=order,
                    total_amount=total_price,
                    payment_id=session.id,  # Use session ID from Stripe
                    payment_status='Payment_Pending',
                )

                return redirect(session.url, code=303)

    context = {
        'items': items,
        'total_price': total_price,
        'addresses': user_addresses,
        'selected_address': selected_address,
    }
    return render(request, 'order/checkout.html', context)


@login_required
def success_view(request, order_id):
    order = get_object_or_404(Orders, id=order_id)

    # Check if the payment method is 'STRIPE' and handle accordingly
    if order.payment_method == 'STRIPE':
        try:
            payment = Payments.objects.get(order=order)
            payment_intent = stripe.PaymentIntent.retrieve(payment.payment_id)
            if payment_intent.status == 'succeeded':
                order.is_paid = True
                payment.payment_status = 'Payment_Succeeded'
                order.save()
                payment.save()
                order.cart.cartitem.all().delete()
                messages.success(request, "Your payment was successful!")
            else:
                messages.warning(request, f"Payment not completed: {payment_intent.status}. Please try again.")
        except Exception as e:
            messages.error(request, f"Error fetching payment status: {str(e)}")
        except stripe.error.InvalidRequestError:
            messages.error(request, "Invalid payment intent. Please contact support.")
        except Payments.DoesNotExist:
            messages.error(request, "Payment record not found for this order.")
        except Exception as e:
            messages.error(request, f"Error fetching payment status: {str(e)}")
    context = {
        'order_id': order.id,
        'payment_method': order.payment_method,
        'total_amount': order.total,
        'order': order
    }

    return render(request, 'order/success.html', context)




@login_required
def add_address(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            return redirect('order:checkout')  # Redirect back to checkout page
    else:
        form = AddressForm()

    context = {
        'form': form,
    }
    return render(request, 'order/addaddress.html', context)


def my_order(request):
    orders = Orders.objects.filter(user=request.user).order_by('-created')
    return render(request,'order/myorder.html',{'orders': orders})


def user_order_track(request, order_id):
   
    order = get_object_or_404(Orders, id=order_id, user=request.user)
    order_status_choices = Orders.ORDER_STATUS 

    return render(request, "order/userordertrack.html", {
        'order': order,
        'order_status_choices': order_status_choices,
       
    })


def change_order_status(request, pid):
   
    order = get_object_or_404(Orders, id=pid)
    status = request.GET.get('status')
  
    allowed_transitions = {
        'Pending': ['Cancelled'],
        'Delivered': ['Return'],
    }

    if status in allowed_transitions.get(order.status, []):
        order.status = status
        order.save()
        messages.success(request, f"Order status updated to '{status}'.")
    else:
        messages.error(request, f"Cannot change status from '{order.status}' to '{status}'.")

    return redirect('order:my_order')


def request_return(request, order_id):
    order = get_object_or_404(Orders, id=order_id, user=request.user)

    # Only allow return requests if the order is delivered and not already requested
    if order.is_paid:
        if order.status == "Delivered" and not order.return_requested and not order.is_refunded:
            order.return_requested = True
            order.save()
            messages.success(request, "Return request submitted successfully.")
    else:
        messages.error(request, "payment not comlted")

    return redirect('order:my_order')  # Change to your dashboard URL