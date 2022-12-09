from django.db import models
from account.models import CustomUser
from django.forms import model_to_dict


class Product(models.Model):
    product_name = models.CharField(max_length=100, null=False, blank=False)
    price = models.DecimalField(max_digits=19, decimal_places=2, null=False, blank=False)
    quantity = models.IntegerField(null=True, blank=False)
    date_and_time_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-product_name',)

    def __str__(self):
        return self.product_name

    @property
    def orders(self):
        return self.cart_product.all().values()

    @property
    def orders_count(self):
        return self.cart_product.all().values().count()


class Cart(models.Model):
    PRODUCT_STATUS = (
        ('pending', 'Pending'),
        ('delivered', 'Delivered'),
    )

    user = models.ForeignKey(CustomUser, related_name="user", on_delete=models.CASCADE)
    cart_products = models.ForeignKey(Product, related_name="cart_products", on_delete=models.CASCADE)
    product_quantity = models.IntegerField()
    product_cost = models.FloatField(default=0.00)
    date_of_ordering = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=PRODUCT_STATUS, default='pending')

    def __str__(self):
        return f"{CustomUser.objects.get(username=self.user)}'s cart"

    @property
    def cart_content(self):
        return model_to_dict(self.cart_products, fields=['product_name', 'price'])