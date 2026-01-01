from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

# Function: Redirect Homepage ("/") directly to Sign Up
def home_redirect(request):
    return redirect('signup')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inventory/', include('inventory.urls')),
    
    # 🛡️ CAPTCHA Route for Bot Protection
    path('captcha/', include('captcha.urls')),
    
    path('', home_redirect, name='home'),
]

# 🛡️ NEW: Allow Django to serve media files (images) during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)