from django.contrib import admin, messages
from django.shortcuts import redirect
from .models import Order

import paypalrestsdk
import stripe

#Admin Action Functions

def refund(modeladmin,request,queryset):
    order = queryset[0]
    return redirect('/admin/refund/'+str(order.ref_code))
refund.short_description = 'Refund Order'

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
    #readonly_fields = ('thing1','thing2')
    actions = [refund]

admin.site.register(Order, OrderAdmin)


