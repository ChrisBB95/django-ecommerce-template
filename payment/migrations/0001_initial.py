# Generated by Django 2.2.3 on 2019-07-12 03:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=20)),
                ('shipping', models.DecimalField(decimal_places=2, max_digits=10)),
                ('shipping_method', models.CharField(max_length=20)),
                ('shipped', models.BooleanField(default=False)),
                ('tracking_number', models.CharField(blank=True, max_length=255, null=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=20)),
                ('order_items', jsonfield.fields.JSONField(default=dict)),
                ('billing_address_line_1', models.CharField(max_length=255)),
                ('billing_address_line_2', models.CharField(blank=True, max_length=255, null=True)),
                ('billing_city', models.CharField(max_length=255)),
                ('billing_state', models.CharField(max_length=255)),
                ('billing_zip', models.CharField(max_length=5)),
                ('shipping_address_line_1', models.CharField(max_length=255)),
                ('shipping_address_line_2', models.CharField(blank=True, max_length=255, null=True)),
                ('shipping_city', models.CharField(max_length=255)),
                ('shipping_state', models.CharField(max_length=255)),
                ('shipping_zip', models.CharField(max_length=5)),
                ('date_ordered', models.DateTimeField(auto_now_add=True)),
                ('ref_code', models.CharField(max_length=16, unique=True)),
                ('paid', models.BooleanField(default=False)),
                ('charge_id', models.CharField(default='0', max_length=30)),
                ('refunded', models.BooleanField(default=False)),
                ('amount_refunded', models.DecimalField(decimal_places=2, default='0', max_digits=20)),
                ('payment_method', models.CharField(max_length=20)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]