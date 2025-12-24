from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import AuditLog

# 1. Listen for Login
@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    # Get IP Address
    ip = request.META.get('REMOTE_ADDR')
    
    # Record it in the database
    AuditLog.objects.create(
        action="User Logged In",
        user=user,
        ip_address=ip
    )
    print(f"🕵️ LOGGED: {user.username} logged in.")

# 2. Listen for Logout
@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    
    AuditLog.objects.create(
        action="User Logged Out",
        user=user,
        ip_address=ip
    )
    print(f"🕵️ LOGGED: {user.username} logged out.")