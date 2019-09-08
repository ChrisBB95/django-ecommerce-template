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

#User-Model Cart for shops that require user authentication to shop
#Alternatively, a session cart can be used when authentication is not required
class Cart_Item(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    subtotal = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return str(self.quantity) + str(self.product.slug)

def add_to_session_cart(request,product,quantity,subtotal):
    if request.session['cart'][product]:
        current_qty = request.session['cart'][product][0]
        current_subtotal = request.session['cart'][product][1]
        request.session['cart'][product] = (quantity+current_qty,subtotal+current_subtotal)
    else:
        request.session['cart'][product] = (quantity,subtotal)
    
    if request.session['cart'][product][0] > product.stock:
        request.session['cart'][product] = (product.stock,product.stock*product.price)
    pass

def remove_from_session_cart(request,product):
    try:
        del request.session['cart'][product]
    except KeyError:
        print('Product not found in cart')
    pass

def add_to_user_cart(user,product,quantity,subtotal):

    if Cart_Item.objects.filter(owner=user,product=product):
        cart_item = Cart_Item.objects.filter(owner=user,product=product).first()
        cart_item.quantity += quantity
        cart_item.subtotal += (quantity*product.price)
    else:
        cart_item = Cart_Item(owner=user,product=product,quantity=quantity,subtotal=subtotal)
    
    if cart_item.quantity > product.stock:
        cart_item.quantity = product.stock
        cart_item.subtotal = (product.stock*product.price)
    
    cart_item.save()
    pass

def remove_from_user_cart(user,product,quantity,subtotal):
    cart_item = Cart_Item.objects.filter(owner=user,product=product).first()
    cart_item.delete()
    pass