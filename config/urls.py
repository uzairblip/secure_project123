from django.contrib import admin
from django.urls import path, include, re_path
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve # 🛡️ Required to serve CSS when DEBUG=False

# Function: Redirect Homepage ("/") directly to Sign Up
def home_redirect(request):
    return redirect('signup')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inventory/', include('inventory.urls')),
    
    # 🛡️ CAPTCHA Route for Bot Protection (OWASP Anti-Automation)
    path('captcha/', include('captcha.urls')),
    
    path('', home_redirect, name='home'),
]

# 🛡️ MANDATORY FOR PRODUCTION (DEBUG=False)
# This allows the server to find your CSS/Images even when debug is off
urlpatterns += [
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

# 🛡️ CUSTOM ERROR HANDLERS (OWASP ASVS V7 compliance)
# These point to the views in your inventory/views.py 
handler404 = 'inventory.views.custom_404'
handler403 = 'inventory.views.custom_403'