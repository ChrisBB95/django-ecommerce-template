from django.contrib import admin
from .models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ['owner', 'ref_code', 'shipping_method', 'tracking_number', 'shipped', 'payment_method',
                    'paid', 'refunded', 'total', 'date_ordered']
    fieldsets = [
        (None, {'fields': ('owner', 'order_items', 'subtotal',
                           'shipping', 'total', 'payment_method', 'paid', 'refunded','amount_refunded', 'shipping_method', 'shipped', 'ref_code', 'charge_id')}),
        ('Billing', {'fields': ('billing_address_line_1', 'billing_address_line_2',
                                'billing_city', 'billing_state', 'billing_zip')}),
        ('Shipping', {'fields': ('tracking_number', 'shipping_address_line_1', 'shipping_address_line_2',
                                 'shipping_city', 'shipping_state', 'shipping_zip')})
    ]
    #readonly_fields = ('owner', 'order_items', 'subtotal', 'shipping', 'shipping_method', 'shipped', 'total', 'payment_method', 'paid', 'refunded','amount_refunded', 'ref_code', 'charge_id', 'billing_address_line_1', 'billing_address_line_2', 'billing_city',
    #                   'billing_state', 'billing_zip', 'shipping_address_line_1', 'shipping_address_line_2', 'shipping_city', 'shipping_state', 'shipping_zip')

admin.site.register(Order, OrderAdmin)