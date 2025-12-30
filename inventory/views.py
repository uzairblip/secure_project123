import sys  # <--- NEW IMPORT FOR NUCLEAR PRINTING
import csv
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, update_session_auth_hash 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm 
from .forms import ProductForm, SignUpForm 
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponse
from .models import Product, AuditLog 

# --- HELPER: GENERATE TOKEN ---
def generate_token():
    return str(random.randint(100000, 999999))

# --- HELPER: PERMISSION CHECKS (RBAC) ---
def is_admin(user):
    return user.is_superuser

def is_staff_or_admin(user):
    return user.is_superuser or user.groups.filter(name='Staff').exists()

# =========================================
# 1. INVENTORY MANAGEMENT
# =========================================

@login_required
def inventory_list(request):
    products = Product.objects.all()
    
    # Search Logic
    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    return render(request, 'inventory/inventory_list.html', {'products': products})

@login_required
@user_passes_test(is_staff_or_admin)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            AuditLog.objects.create(user=request.user, action="Added Item", target=product.name)
            return redirect('inventory_list')
    else:
        form = ProductForm()
    return render(request, 'inventory/add_product.html', {'form': form})

@login_required
@user_passes_test(is_staff_or_admin)
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            AuditLog.objects.create(user=request.user, action="Edited Item", target=product.name)
            return redirect('inventory_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'inventory/add_product.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    AuditLog.objects.create(user=request.user, action="Deleted Item", target=product.name)
    product.delete()
    return redirect('inventory_list')

# 👇 CSV EXPORT FUNCTION 👇
@login_required
@user_passes_test(is_staff_or_admin)
def export_inventory_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventory_report.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Product Name', 'Quantity', 'Price', 'Added By']) # Header
    
    products = Product.objects.all()
    for product in products:
        writer.writerow([product.name, product.quantity, product.price, product.created_by.username])
    
    AuditLog.objects.create(user=request.user, action="Exported Data", target="All Inventory (CSV)")
    return response

# =========================================
# 2. SYSTEM ADMIN (USERS & LOGS)
# =========================================

@login_required
@user_passes_test(is_admin)
def audit_log_view(request):
    logs = AuditLog.objects.all().order_by('-timestamp')
    return render(request, 'inventory/audit_log.html', {'logs': logs})

# 👇 USER LIST VIEW 👇
@login_required
@user_passes_test(is_admin)
def user_list_view(request):
    # Show all users EXCEPT the Superuser (to prevent accidents)
    users = User.objects.all().exclude(is_superuser=True)
    return render(request, 'inventory/user_list.html', {'users': users})

# 👇 PROMOTE/DEMOTE STAFF 👇
@login_required
@user_passes_test(is_admin)
def toggle_staff_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # Flip the status
    user.is_staff = not user.is_staff
    user.save()
    
    status_msg = "Promoted to Staff" if user.is_staff else "Demoted to User"
    AuditLog.objects.create(user=request.user, action=status_msg, target=user.username)
    
    return redirect('user_list')

# 👇 DELETE USER 👇
@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    AuditLog.objects.create(user=request.user, action="Deleted User", target=user.username)
    user.delete()
    return redirect('user_list')

# =========================================
# 3. SECURE REGISTRATION & LOGIN
# =========================================

def register_view_safe(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False 
            user.email = form.cleaned_data['email']
            user.save()
            token = generate_token()
            request.session['reg_user_id'] = user.id
            request.session['reg_token'] = token
            send_mail('Verify Your Account', f'Your token: {token}', 'uzairsamsudin123@gmail.com', [user.email], fail_silently=False)
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

def custom_login(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if not user.is_active:
                messages.error(request, "Account not verified.")
                return redirect('login')
            
            # ✅ LOG SUCCESS: We know the user exists, so we save to DB
            AuditLog.objects.create(
                user=user, 
                action="Login Challenge", 
                target="2FA Started"
            )

            token = generate_token()
            request.session['login_user_id'] = user.id
            request.session['login_token'] = token
            send_mail('Login Token', f'Your 2FA token: {token}', 'uzairsamsudin123@gmail.com', [user.email], fail_silently=False)
            return redirect('verify_login')
        else:
            # 🚨 LOG FAILURE: FORCE OUTPUT TO TERMINAL (NO BUFFERING)
            failed_user = request.POST.get('username', 'Unknown')
            
            # This writes directly to the error stream (Usually RED text)
            sys.stderr.write(f"\n{'='*40}\n")
            sys.stderr.write(f"⚠️  SECURITY ALERT: FAILED LOGIN -> {failed_user}\n")
            sys.stderr.write(f"{'='*40}\n")
            
            messages.error(request, "Invalid credentials.")
            
    return render(request, 'registration/login.html')

def verify_login(request):
    if request.method == 'POST':
        entered_token = request.POST['token']
        if entered_token == request.session.get('login_token'):
            user_id = request.session.get('login_user_id')
            if not user_id:
                return redirect('login')
            user = User.objects.get(id=user_id)
            login(request, user)
            request.session.pop('login_user_id', None)
            request.session.pop('login_token', None)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid 2FA Token.")
    return render(request, 'registration/verify_token.html')

@login_required
def dashboard_view(request):
    total_products = Product.objects.count()
    low_stock = Product.objects.filter(quantity__lt=5).count()
    context = {'total_products': total_products, 'low_stock': low_stock}
    return render(request, 'inventory/dashboard.html', context)

# =========================================
# 4. USER PROFILE SYSTEM (NEW!)
# =========================================

@login_required
def profile_view(request):
    # Get last 5 actions for "Recent Activity"
    user_logs = AuditLog.objects.filter(user=request.user).order_by('-timestamp')[:5]
    context = {'user_logs': user_logs}
    return render(request, 'inventory/profile.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            
            AuditLog.objects.create(
                user=request.user, 
                action="Changed Password", 
                target="Self"
            )
            
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
        
    return render(request, 'registration/change_password.html', {'form': form})

# =========================================
# 5. ERROR HANDLERS
# =========================================

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_403(request, exception):
    return render(request, '403.html', status=403)