from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#views imports
from home.views import home, contact, cart
from shop.views import shop, product
from payment.views import checkout, process, checkout_complete, checkout_canceled

urlpatterns = [
    path('admin', admin.site.urls),
    path('', home, name='home'),
    path('home', home, name='home'),
    path('contact', contact, name='contact'),
    path('cart', cart, name='cart'),
    path('shop', shop, name='shop'),
    path('shop/<item_slug>', shop, name='product'),
    path('checkout', checkout, name='checkout'),
    path('checkout/process', process, name='process'),
    path('checkout/complete', checkout_complete, name='checkout_complete'),
    path('checkout/canceled', checkout_canceled, name='checkout_canceled'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)