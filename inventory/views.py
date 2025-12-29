import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
# Note: We now import SignUpForm instead of UserCreationForm
from .forms import ProductForm, SignUpForm 
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Product

# --- HELPER: GENERATE TOKEN ---
def generate_token():
    return str(random.randint(100000, 999999))

# --- HELPER: PERMISSION CHECKS (RBAC) ---
def is_admin(user):
    """Checks if user is a Superuser (Admin)"""
    return user.is_superuser

def is_staff_or_admin(user):
    """Checks if user is Admin OR in the 'Staff' group"""
    return user.is_superuser or user.groups.filter(name='Staff').exists()

# =========================================
# 1. INVENTORY MANAGEMENT (RBAC APPLIED)
# =========================================

@login_required
def inventory_list(request):
    """
    ACCESS: Admin, Staff, and Normal Users
    Everyone who is logged in can VIEW the list.
    """
    products = Product.objects.all()
    return render(request, 'inventory/inventory_list.html', {'products': products})

@login_required
@user_passes_test(is_staff_or_admin) # <--- CHANGED: Allows Staff & Admin
def add_product(request):
    """
    ACCESS: Admin and Staff Only
    Normal users cannot access this page.
    """
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            return redirect('inventory_list')
    else:
        form = ProductForm()
    return render(request, 'inventory/add_product.html', {'form': form})

@login_required
@user_passes_test(is_admin) # <--- KEPT: Only Admin can delete
def delete_product(request, product_id):
    """
    ACCESS: Admin Only
    Staff and Normal Users cannot delete items.
    """
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('inventory_list')

# =========================================
# 2. SECURE REGISTRATION (Dynamic Email)
# =========================================

def register_view_safe(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Create user but DEACTIVATE them
            user = form.save(commit=False)
            user.is_active = False 
            user.email = form.cleaned_data['email'] # Save email to DB
            user.save()
            
            # Generate Token
            token = generate_token()
            request.session['reg_user_id'] = user.id
            request.session['reg_token'] = token
            
            # Get the email the user just typed
            user_email = form.cleaned_data['email']

            print(f"--- REGISTRATION TOKEN: {token} ---")
            
            # SEND REAL EMAIL
            send_mail(
                'Verify Your Account',
                f'Your registration token is: {token}',
                'uzairsamsudin123@gmail.com',    # <--- SENDER EMAIL (You)
                [user_email],                    # <--- RECEIVER (The User)
                fail_silently=False,
            )
            
            return redirect('verify_registration')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})

def verify_registration_safe(request):
    if request.method == 'POST':
        entered_token = request.POST['token']
        if entered_token == request.session.get('reg_token'):
            user_id = request.session.get('reg_user_id')
            user = User.objects.get(id=user_id)
            
            user.is_active = True 
            user.save()
            
            messages.success(request, "Account Verified! Please Login.")
            return redirect('login')
        else:
            messages.error(request, "Invalid Token.")
    return render(request, 'registration/verify_token.html')

# =========================================
# 3. 2FA LOGIN (Dynamic Email)
# =========================================

def custom_login(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        
        if user is not None:
            if not user.is_active:
                messages.error(request, "Account not verified.")
                return redirect('login')
                
            token = generate_token()
            request.session['login_user_id'] = user.id
            request.session['login_token'] = token
            
            print(f"--- LOGIN 2FA TOKEN: {token} ---")
            
            # SEND REAL EMAIL
            send_mail(
                'Your Login Token',
                f'Your 2FA token is: {token}',
                'uzairsamsudin123@gmail.com',  # <--- FIXED: Now uses your real email
                [user.email],                  # <--- FIXED: Sends to the user's saved email
                fail_silently=False,
            )
            
            return redirect('verify_login')
        else:
            messages.error(request, "Invalid credentials.")
            
    return render(request, 'registration/login.html')

def verify_login(request):
    if request.method == 'POST':
        entered_token = request.POST['token']
        if entered_token == request.session.get('login_token'):
            user_id = request.session.get('login_user_id')
            user = User.objects.get(id=user_id)
            
            login(request, user)
            
            del request.session['login_user_id']
            del request.session['login_token']
            
            # <--- FIXED: Redirects to Dashboard now!
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid 2FA Token.")
            
    return render(request, 'registration/verify_token.html')

# --- DASHBOARD VIEW ---
@login_required
def dashboard_view(request):
    return render(request, 'inventory/dashboard.html')