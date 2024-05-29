from django.db import models
from django.contrib.auth.models import User
class Address(models.Model):
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=2)
    postcode = models.CharField(max_length=100)

    def __str__(self):
        return " ".join([self.street, self.city, self.state, str(self.postcode)])

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def cart(self):
        return CartItem.objects.filter(customer=self)

class BillingAddress(Address):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    shippingaddress = models.OneToOneField(Address, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.customer) + " @ " + str(self.shippingaddress)

class OrderPayment(models.Model):
    cardNumber = models.BigIntegerField()
    txnId = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    billingaddress = models.ForeignKey(BillingAddress, on_delete=models.CASCADE)

class Product(models.Model):
    name = models.CharField(max_length=100)
    image= models.ImageField()
    price=models.FloatField()
    category=models.CharField(max_length=100)
    stock=models.IntegerField(default=30)


class OrderItem(models.Model):
    price = models.FloatField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
class CartItem(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Default quantity is 1
class PaymentandShipping2(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=2)
    postcode = models.CharField(max_length=100)
    cardNumber = models.BigIntegerField()
    items_bought = models.ManyToManyField(CartItem)
    cardNumber = models.BigIntegerField()
    total_price = models.FloatField(default=0)
    item_details = models.TextField(default="")

    