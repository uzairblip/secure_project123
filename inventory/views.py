from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Product

# Security Check: Is the user an Admin (Superuser)?
def is_admin(user):
    return user.is_superuser

@login_required
def inventory_list(request):
    # Everyone can VIEW the list
    products = Product.objects.all()
    return render(request, 'inventory/inventory_list.html', {'products': products})

@login_required
@user_passes_test(is_admin)  # <--- THIS IS THE NEW SECURITY LOCK
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        
        Product.objects.create(
            name=name,
            quantity=quantity,
            price=price,
            created_by=request.user
        )
        return redirect('inventory_list')
    
    return render(request, 'inventory/add_product.html')