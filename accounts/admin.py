from django.contrib import admin
from .models import AuditLog

# Configure how the logs look in the Admin Panel
@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'user', 'timestamp', 'ip_address') # Columns to show
    list_filter = ('action', 'timestamp') # Sidebar filters
    search_fields = ('user__username', 'action') # Search box
    readonly_fields = ('action', 'user', 'timestamp', 'ip_address') # Make them Read-Only (Security!)