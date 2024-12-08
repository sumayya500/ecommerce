# admindashboard/views.py
from venv import logger
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from product.models import Product, Category
from product.forms import ProductForm
from django.urls import reverse
from django.contrib import messages
from order.models import Orders,Payments
from django.db.models.functions import Coalesce
from django.utils.safestring import mark_safe 
import json
from django.db.models import Sum

def admin_required(user):
    return user.is_staff 



@login_required
@user_passes_test(admin_required)
def admin_dashboard(request):
    return render(request, 'admindashboard/admindashboard.html')



def admin_view(request):
  
    total_orders = Orders.objects.count()
    total_categories = Category.objects.count()
    total_products = Product.objects.count()
    total_users = CustomUser.objects.count()
    cod_payment = Orders.objects.filter(payment_method='COD', is_paid=True).aggregate(total=Sum('total'))['total'] or 0
    stripe_payment = Orders.objects.filter(payment_method='STRIPE', is_paid=True).aggregate(total=Sum('total'))['total'] or 0

    total_revenue = cod_payment + stripe_payment

    context = {
        'total_orders': total_orders,
        'total_categories': total_categories,
        'total_products': total_products,
        'total_users': total_users,
        'cod_payment': cod_payment,
        'stripe_payment': stripe_payment,
        'total_revenue': total_revenue,
    }

    return render(request, 'admindashboard/adminview.html', context)



def user_management(request):
    users = CustomUser.objects.all()
    return render(request,'admindashboard/usermanagment.html',{'users':users})


def activate_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = True
    user.save()
    return redirect('admindashboard:user_management')

def deactivate_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = False
    user.save()
    return redirect('admindashboard:user_management')

def logout_view(request):
    return redirect('admindashboard:admin_dashboard')  

def product_dashboard(request):
    products = Product.objects.all()
    return render(request, 'admindashboard/productdashboard.html', {'products': products})




def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            form.save()  # Save the new product
            return redirect('admindashboard:product_dashboard')  # Redirect to product dashboard after saving
    else:
        form = ProductForm()  # Create an empty form for GET requests

    return render(request, 'admindashboard/addproduct.html', {'form': form})  # R



def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Get the product by ID

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)  # Bind the form to the product instance
        if form.is_valid():
            form.save()  # Save the updated product data
            return redirect('admindashboard:product_dashboard')  # Redirect to the product dashboard after saving
    else:
        form = ProductForm(instance=product)  # Populate the form with existing product data

    return render(request, 'admindashboard/editproduct.html', {'form': form, 'product': product})  # Render the edit template


def delete_product(request, product_id):
    # Get the product by ID, or return a 404 error if it doesn't exist
    product = get_object_or_404(Product, id=product_id)
    
    # Check if the request method is POST (to confirm deletion)
    if request.method == 'POST':
        product.delete()  # Delete the product
        messages.success(request, 'Product deleted successfully.')  # Add a success message
        return redirect('admindashboard:product_dashboard')  # Redirect to the product dashboard
    
    return render(request, 'admindashboard/deleteproduct.html', {'product': product})  # Render a confirmation page if not POST


User = get_user_model()


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'admindashboard/categorylist.html', {'categories': categories})



# Add Category (No Form)
def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('categoryname')
        if category_name:
            Category.objects.create(categoryname=category_name)
            return redirect('category_list')
    return render(request, 'admindashboard/categoryadd.html')

# Edit Category (No Form)
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category_name = request.POST.get('categoryname')
        if category_name:
            category.categoryname = category_name
            category.save()
            return redirect('category_list')
    return render(request, 'admindashboard/categoryedit.html', {'category': category})

# Delete Category
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'admindashboard/categorydelete.html', {'category': category})

def admin_order(request):
    # Toggle is_paid status if order_id is provided in GET request
    order_id = request.GET.get('order_id')
    if order_id:
        try:
            order = Orders.objects.get(id=order_id)
            order.is_paid = not order.is_paid
            order.save()
        except Orders.DoesNotExist:
            pass  # Handle the case where the order does not exist

        return redirect(reverse('admindashboard:admin_order'))

    # Render the orders page with all orders
    orders = Orders.objects.select_related('address', 'cart', 'user').order_by('-created').all()
    return render(request, 'admindashboard/admin_order.html', {'orders': orders})


def admin_update_order_status(request):
    if request.method == "POST":
        orders = Orders.objects.all()
        for order in orders:
            new_status = request.POST.get(f"status_{order.id}")
            if new_status and new_status != order.status:
                order.status = new_status
                order.save()
                messages.success(request, f"Order {order.id} status updated to {new_status}.")
        return redirect('admindashboard:admin_order')
    return redirect('admin_order')

def approve_return(request, order_id):
    order = get_object_or_404(Orders, id=order_id)

    
    if not request.user.is_staff:
        messages.error(request, "Permission denied: Only staff can approve returns.")
        return redirect('admin_order')

    # Check if return request conditions are met
    if not order.return_requested:
        messages.error(request, "Return request not initiated for this order.")
        return redirect('admin_order')

    if order.return_approved:
        messages.error(request, "This order's return has already been approved.")
        return redirect('admin_order')

    if order.is_refunded:
        messages.error(request, "This order has already been refunded.")
        return redirect('admin_order')

    try:

        # Handle wallet update if order was paid
        if order.is_paid:

            order.return_approved = True
            order.status = "Returned"
            order.is_refunded = True  # Mark as refunded
            order.save()
            # Update user's wallet
            order.user.wallet += order.total
            order.user.save()
            messages.success(request, "Return request approved and amount added to wallet.")
            logger.info(f"Return approved for Order ID {order_id}. Wallet updated for user {order.user.id}.")
        else:
            messages.warning(request, "Order was not paid. No amount added to wallet.")

        # Additional logging

    except Exception as e:
        messages.error(request, f"An error occurred while approving the return: {e}")

    return redirect('admin_order')
