from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField

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