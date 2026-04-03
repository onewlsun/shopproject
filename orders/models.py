from django.db import models
from django.conf import settings

class Order(models.Model):
    first_name = models.CharField(max_length=50, default="Имя")
    last_name = models.CharField(max_length=50, default="Фамилия")
    phone = models.CharField(max_length=20)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="orders_orders"  # уникальное имя
    )
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    STATUS_CHOICES = [
        ("new", "Новый"),
        ("processing", "В обработке"),
        ("done", "Выполнен"),
        ("canceled", "Отменён"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product} x {self.quantity}"