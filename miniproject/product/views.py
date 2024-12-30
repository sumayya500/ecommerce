from django.shortcuts import render,redirect,get_object_or_404
from product.forms import ProductForm
from django.contrib import messages
from .models import Product,Category,Wishlist
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            return redirect('/product')
          
        else:
            print(form.errors) 
    else:
        form = ProductForm()
    products = Product.objects.all()
    
    context = {'form': form,
             'Products': products   
             
        }

    return render(request, 'product/add_product.html', context)


def product_search(request):
    query = request.GET.get('q', '')  # Get the search query from the request
    category_query = request.GET.get('category', '')  # Get the category query from the request
    
    # Base queryset
    products = Product.objects.all()
    
    # Apply search query filter
    if query:
        products = products.filter(name__icontains=query)
    
    # Apply category filter if provided
    if category_query:
        products = products.filter(category__categoryname__icontains=category_query)  # Assuming `category` is a related field
    
    # Check if any products were found
    no_products_message = None
    if not products.exists():  # No products found
        no_products_message = "No products available for your search."
    
    context = {
        'query': query,
        'category_query': category_query,
        'products': products,
        'no_products_message': no_products_message,
    }
    return render(request, 'accounts/index.html', context)






# @login_required
# def product_detail_view(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     context = {
#         'product': product,
#         'is_in_wishlist': product in request.user.wishlist.all()  # check if product is in wishlist
#     }
#     return render(request, 'product/productdetail.html', context)

# def product_detail_view(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     is_in_wishlist = request.user.is_authenticated and product in request.user.wishlist.all()
#     context = {
#         'product': product,
#         'is_in_wishlist': is_in_wishlist,
#     }
#     return render(request, 'product/productdetail.html', context)


def product_detail_view(request, product_id):
    # Retrieve the product or show a 404 error if not found
    product = get_object_or_404(Product, id=product_id)
    
    context = {
        'product': product,
    }
    return render(request, 'product/productdetail.html', context)

def category_view(request, category_name):
    category = get_object_or_404(Category, categoryname=category_name)
    products = Product.objects.filter(category=category)
    context = {
        'category_name': category_name,
        'products': products,
    }
    return render(request, 'product/category.html', context)


@login_required(login_url='/login')
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'product/wishlist.html', {'wishlist_items': wishlist_items, 'product':product})

@login_required(login_url='/login')
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if Wishlist.objects.filter(user=request.user, product=product).exists():
        messages.info(request, f"{product.name} is already in your wishlist.")
    else:
        Wishlist.objects.create(user=request.user, product=product)
        messages.success(request, f"{product.name} added to your wishlist.")
    return redirect('product:wishlist') 


def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product)
    if wishlist_item.exists():
        wishlist_item.delete() 
        messages.success(request, f"{product.name} removed from your wishlist.")
    else:
        messages.info(request, f"{product.name} is not in your wishlist.")
    return redirect('product:wishlist') 
