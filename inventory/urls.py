from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # --- DASHBOARD ---
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # --- INVENTORY SYSTEM ---
    path('', views.inventory_list, name='inventory_list'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('export/', views.export_inventory_csv, name='export_inventory'),

    # --- SYSTEM ADMIN (LOGS & USERS) ---
    path('history/', views.audit_log_view, name='audit_log'),
    path('users/', views.user_list_view, name='user_list'),
    path('users/promote/<int:user_id>/', views.toggle_staff_status, name='toggle_staff'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),

    # --- 👤 NEW: PROFILE & SETTINGS ---
    path('profile/', views.profile_view, name='profile'),
    path('profile/password/', views.change_password, name='change_password'),

    # --- AUTHENTICATION ---
    path('accounts/signup/', views.register_view_safe, name='signup'),
    path('accounts/signup/verify/', views.verify_registration_safe, name='verify_registration'),
    path('accounts/login/', views.custom_login, name='login'),
    path('accounts/login/verify/', views.verify_login, name='verify_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]