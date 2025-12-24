from django.db import models
from django.contrib.auth.models import User

# THIS IS THE MISSING PART CAUSING THE ERROR
class AuditLog(models.Model):
    action = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True)

    def __str__(self):
        return f"{self.user.username} - {self.action}"