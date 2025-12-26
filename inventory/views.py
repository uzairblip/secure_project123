from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Product
from .forms import ProductForm  # <--- IMPORT THE NEW FORM HERE

# Security Check: Is the user an Admin (Superuser)?
def is_admin(user):
    return user.is_superuser

@login_required
def inventory_list(request):
    products = Product.objects.all()
    return render(request, 'inventory/inventory_list.html', {'products': products})

@login_required
@user_passes_test(is_admin)
def add_product(request):
    # 1. If the user clicked "Save" (POST request)
    if request.method == 'POST':
        form = ProductForm(request.POST) # Fill the form with their data
        if form.is_valid():
            product = form.save(commit=False) # Pause saving to add the user
            product.created_by = request.user # Add the logged-in user
            product.save() # Now save to DB
            return redirect('inventory_list')
            
    # 2. If the user just opened the page (GET request)
    else:
        form = ProductForm() # Create a blank form

    # 3. CRITICAL: Send the 'form' to the template!
    return render(request, 'inventory/add_product.html', {'form': form})