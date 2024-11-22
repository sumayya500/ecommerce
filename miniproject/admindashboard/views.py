# admindashboard/views.py
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from product.models import Product, Category
from product.forms import ProductForm
from django.urls import reverse
from django.contrib import messages



def admin_required(user):
    return user.is_staff  



@login_required
@user_passes_test(admin_required)
def admin_dashboard(request):
    return render(request, 'admindashboard/admindashboard.html')

User = get_user_model()

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

def profile(request):
    return render(request, 'admindashboard/profile.html', {'user': request.user})

def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        if 'phone_number' in request.POST:  # Check if the field exists
            user.phone_number = request.POST.get('phone_number')  # Assuming you have this field
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')

    return render(request, 'admindashboard/edit_profile.html', {'user': user})

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