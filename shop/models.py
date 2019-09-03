from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=255,db_index=True)
    slug = models.SlugField(max_length=255,db_index=True)
    item_number = models.PositiveIntegerField(unique=True)

    image_1 = models.ImageField(upload_to='products/%y/%m/%d', blank=True)
    image_2 = models.ImageField(upload_to='products/%y/%m/%d', blank=True)
    image_3 = models.ImageField(upload_to='products/%y/%m/%d', blank=True)

    description = models.TextField(blank=True,null=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ('item_number',)
        index_together = (('id', 'slug'))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.id, self.slug])

class Cart_Item(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    subtotal = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return str(self.owner.id)