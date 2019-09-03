from django.template.loader import render_to_string, get_template
from django.contrib import admin, messages
from django.utils.html import strip_tags
from django.shortcuts import redirect
from django.conf import settings
from django.core import mail

from .models import Order

import paypalrestsdk
import stripe

#Admin Action Functions

def refund(modeladmin,request,queryset):
    order = queryset[0]
    return redirect('/admin/refund/'+str(order.ref_code))
refund.short_description = 'Refund Order'

def mark_shipped(modeladmin, request, queryset):
    queryset.update(shipped=True)
    for order in queryset:
        order_items = order.order_items
        tracking_numbers = order.tracking_number.split(',')
        email_context = {
            'owner': order.owner,
            'ref_code': order.ref_code,
            'billing_address_line_1': order.billing_address_line_1,
            'billing_address_line_2': order.billing_address_line_2,
            'billing_city': order.billing_city,
            'billing_state': order.billing_state,
            'billing_zip': order.billing_zip,
            'shipping_address_line_1': order.shipping_address_line_1,
            'shipping_address_line_2': order.shipping_address_line_2,
            'shipping_city': order.shipping_city,
            'shipping_state': order.shipping_state,
            'shipping_zip': order.shipping_zip,
            'order_items': order_items,
            'shipping': order.shipping,
            'subtotal': order.subtotal,
            'total': order.total,
            'shipping_method': order.shipping_method,
            'tracking_numbers': tracking_numbers,
            'in_store': order.shipping_method == 'In-Store Pickup',
        }
        subject = '###### - Your Order Has Shipped!'
        html_msg = render_to_string(
            'payment/shipping_confirmation.html', context=email_context)
        plain_msg = strip_tags(html_msg)
        mail.send_mail(subject, plain_msg, from_email=settings.DEFAULT_FROM_EMAIL,
                       recipient_list=[order.owner.email], fail_silently=False, html_message=html_msg)
        
        staff_subject = '###### - Order Shipped'
        email_context['staff'] = True
        html_msg = render_to_string(
            'payment/shipping_confirmation.html', context=email_context)
        plain_msg = strip_tags(html_msg)
        mail.send_mail(staff_subject, plain_msg, from_email=settings.DEFAULT_FROM_EMAIL,
                       recipient_list=['######'], fail_silently=False, html_message=html_msg)
mark_shipped.short_description = 'Mark Order As Shipped'

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
    actions = [refund,mark_shipped]

admin.site.register(Order, OrderAdmin)


