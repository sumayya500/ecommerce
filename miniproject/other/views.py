from django.shortcuts import render,redirect,get_object_or_404
from product.forms import ProductForm 
from product.models import Product,Category

def blog(request):
    return render(request, 'other/blog.html')

def contact(request):
    return render(request, 'other/contact.html')

def shop(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request,'other/shop.html',context)


def product_search(request):
    query = request.GET.get('q', '')  # Get the search query from the request
    products = Product.objects.filter(name__icontains=query) if query else []  # Search by name
    

    no_products_message = "No products available for your search." if not products.exists() else None
    
    context = {
        'query': query,
         'products': products,
        'no_products_message': no_products_message,
    }
    return render(request, 'other/shop.html', context)



def filter_by_category(request, category_name):
    category_name = category_name.replace('%20', ' ')  # Convert URL-encoded spaces to normal spaces
    category = get_object_or_404(Category, categoryname=category_name)  # Ensure category exists
    products = Product.objects.filter(category=category)
    return render(request, 'products/category_list.html', {'products': products, 'category': category_name})