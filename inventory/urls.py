from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # --- DASHBOARD (THE NEW HOME PAGE) ---
    path('dashboard/', views.dashboard_view, name='dashboard'), # <--- NEW ADDITION

    # --- INVENTORY SYSTEM ---
    path('', views.inventory_list, name='inventory_list'),
    path('add/', views.add_product, name='add_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),

    # --- SECURE AUTHENTICATION ---
    path('accounts/signup/', views.register_view_safe, name='signup'),
    path('accounts/signup/verify/', views.verify_registration_safe, name='verify_registration'),
    
    path('accounts/login/', views.custom_login, name='login'),
    path('accounts/login/verify/', views.verify_login, name='verify_login'),

    # --- LOGOUT ---
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]