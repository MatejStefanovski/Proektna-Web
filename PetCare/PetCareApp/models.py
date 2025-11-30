from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    LABEL_CHOICES = [
        ('oprema', 'Oprema'),
        ('igracki', 'Igracki'),
        ('milenicinja', 'Milenicinja'),
        ('hrana', 'Hrana'),
        ('nega', 'Nega'),
    ]
    label = models.CharField(max_length=20, choices=LABEL_CHOICES)

    def __str__(self):
        return self.name

class Veterinarian(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    image = models.ImageField(upload_to='veterinarians/', blank=True, null=True)
    experience_years = models.PositiveIntegerField()
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'product']

    def __str__(self):
        return f"{self.user.username} - {self.product.name} (x{self.quantity})"

    @property
    def subtotal(self):
        return self.product.price * self.quantity
