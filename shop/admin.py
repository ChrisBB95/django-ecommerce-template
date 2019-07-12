from django.contrib import admin
from .models import Product, Cart_Item

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'item_number', 'price', 'stock', 'available']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['item_number', 'price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['item_number', 'name']
    fieldsets = (
        ('Product',{'fields':('name','slug','item_number','description')}),
        ('Details',{'fields':('price','stock','available')}),
        ('Images',{'fields':('image_1','image_2','image_3')}),
    )

admin.site.register(Product, ProductAdmin)