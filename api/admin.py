from django.contrib import admin

from api.models import Customer, Product, ProductionCapability, Batch, Policy

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(ProductionCapability)
admin.site.register(Batch)
admin.site.register(Policy)
