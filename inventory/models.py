from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Who added this item? (Good for auditing/security logs)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name} (Qty: {self.quantity})"
