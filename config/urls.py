from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# Function: Redirect Homepage ("/") directly to Sign Up
def home_redirect(request):
    return redirect('signup')  # <--- CHANGED THIS to 'signup'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('inventory/', include('inventory.urls')),
    path('', home_redirect, name='home'),
]