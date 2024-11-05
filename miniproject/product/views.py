from django.shortcuts import render,redirect
from product.forms import ProductForm
from django.contrib import messages
from .models import Product


def product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # Include request.FILES for file uploads
        if form.is_valid():
            form.save()
            return redirect('/product')
          
        else:
            print(form.errors)  # Print form errors for debugging purposes
    else:
        form = ProductForm()
    products = Product.objects.all()
    
    context = {'form': form,
             'Products': products   
             
        }

    return render(request, 'product/add_product.html', context)