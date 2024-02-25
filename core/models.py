from django.db import models
from django.contrib.auth import get_user_model
import os
from django.utils import timezone
import uuid
User = get_user_model()


def get_product_cover(instance, filename):
    base_path = timezone.now().strftime('products/%Y/%m/%d')
    filename, ext = os.path.splitext(os.path.basename(filename))
    new_filename = uuid.uuid5(uuid.NAMESPACE_URL, filename)
    out = os.path.join(base_path,f'{new_filename}{ext}')
    return out


class My_model(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:

        abstract = True


class Customer(My_model):
    name = models.CharField(max_length=150)
    family = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f'{self.name}, {self.slug}'


class Order(My_model):
    id = models.AutoField(primary_key=True)
    createdate = models.DateField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user')


    def __str__(self):
        return f'{self.createdate}'


class Product(My_model):
    name = models.CharField(max_length=150)
    price = models.IntegerField()
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=get_product_cover, blank=True, null=True)

    def __str__(self):
        return f'{self.name}, {self.slug}'


class OrderItem(My_model):
    id = models.AutoField(primary_key=True)
    Qty = models.IntegerField()
    discount = models.IntegerField(null=True, blank=True)
    total_price = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.order}'


