from django.db import models
from django.contrib.auth.models import User

# --- NEW: CATEGORY TABLE (Feature #2) ---
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# --- UPDATED: PRODUCT TABLE ---
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    # 🛡️ NEW FIELDS for Feature #2
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='inventory_images/', null=True, blank=True)
    
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Who added this item? (Good for auditing/security logs)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name} (Qty: {self.quantity})"

# --- AUDIT LOG TABLE ---
class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50)  # e.g., "Added", "Deleted"
    target = models.CharField(max_length=100) # e.g., "iPhone 15"
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"