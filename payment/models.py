from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from jsonfield import JSONField
from django.db import models

from paypalrestsdk import Payment
import stripe

class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order_items = JSONField()
    date_ordered = models.DateTimeField(auto_now_add=True)
    ref_code = models.CharField(max_length=16, unique=True)

    subtotal = models.DecimalField(max_digits=20, decimal_places=2)
    shipping = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=20, decimal_places=2)

    paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=20)
    charge_id = models.CharField(max_length=30, default='0')

    refunded = models.BooleanField(default=False)
    amount_refunded = models.DecimalField(max_digits=20,decimal_places=2,default='0')

    shipped = models.BooleanField(default=False)
    shipping_method = models.CharField(max_length=20)
    tracking_number = models.CharField(max_length=255, blank=True, null=True)

    billing_address_line_1 = models.CharField(max_length=255)
    billing_address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    billing_city = models.CharField(max_length=255)
    billing_state = models.CharField(max_length=255)
    billing_zip = models.CharField(max_length=5)

    shipping_address_line_1 = models.CharField(max_length=255)
    shipping_address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    shipping_city = models.CharField(max_length=255)
    shipping_state = models.CharField(max_length=255)
    shipping_zip = models.CharField(max_length=5)

    def __str__(self):
        return '{0}'.format(self.ref_code)

#requires user to be authenticated
def handle_stripe_payment(request,order):
    order.payment_method = 'Stripe'
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = str(order.total).replace('.', '')
    token = request.POST.get('stripeToken')

    charge = stripe.Charge.create(
        amount=stripe_total,
        currency='usd',
        description=str(request.user.email),
        source=token,
        metadata={'id': order.ref_code}
    )

    charge_id = charge.id
    order.charge_id = charge_id
    order.save()
    return redirect(reverse('checkout_complete'))

def handle_paypal_payment(request,order,cart_items):
    items = [{'name': item.product.name,
            'quantity': item.quantity,
            'price': float(item.subtotal / item.quantity),
            'shipping': '0.00',
            'currency': 'USD'} for item in cart_items]

    items.append({'name': 'shipping', 'quantity': 1,
                'price': float(order.shipping), 'currency': 'USD'})

    payment = Payment({
        'intent': 'sale',
        'payer': {
            'payment_method': 'paypal',
        },
        'redirect_urls': {
            'return_url': 'http://{}{}'.format(host, reverse('payment:done')),
            'cancel_url': 'http://{}{}'.format(host, reverse('payment:canceled')),
        },
        'transactions': [{
            'amount': {
                'total': float(order.total),
                'currency': 'USD',
            },
            'description': order.ref_code,
            'item_list': {
                'items': items
            }
        }],
    })

    if payment.create():
        for link in payment.links:
            if link.method == 'REDIRECT':
                redirect_url = (link.href)
                order.charge_id = payment.id
                order.save()
                return redirect(redirect_url)
    else:
        messages.error(request,'There was an error while processing your payment')
        messages.error(request,str(payment.error))
        pass