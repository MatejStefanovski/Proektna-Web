from django.contrib import admin
from .models import Product, CartItem, Veterinarian

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'label', 'created_at')
    list_filter = ('label',)

admin.site.register(Product, ProductAdmin)
admin.site.register(CartItem)
admin.site.register(Veterinarian)
