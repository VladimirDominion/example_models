from django.db import models
from django_lifecycle import LifecycleModelMixin, hook, AFTER_DELETE, BEFORE_SAVE, AFTER_SAVE

# Create your models here.


class BaseCart(models.Model):
    total_quantity = models.PositiveIntegerField(null=True, default=0, blank=True)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_items(self) -> models.QuerySet:
        raise NotImplementedError('Implement get_items')

    def recalculate(self):
        total_amount = 0
        total_quantity = 0
        for item in self.get_items():
            total_amount += item.amount
            total_quantity += item.quantity
        self.total_amount = total_amount
        self.total_quantity = total_quantity
        self.save()

    class Meta:
        abstract = True


class BaseCartItem(LifecycleModelMixin, models.Model):
    quantity = models.PositiveIntegerField(null=True, blank=True, default=0)
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    class Meta:
        abstract = True


class OrderRang(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            rang=models.Case(
                models.When(total_amount__lt=50, then=models.Value('Small')),
                models.When(
                    models.Q(total_amount__gte=50) & models.Q(total_amount__lt=150)
                    , then=models.Value('Middle')),
                models.When(total_amount__gte=150, then=models.Value('Big')),
                default=models.Value('None'),
                output_field=models.CharField(),
            )
        )
        return queryset


class Order(BaseCart):
    class OrderStatus(models.TextChoices):
        NEW = 'NEW', 'New'
        PAID = 'PAID', 'Paid'
        CANCELED = 'CANCELED', 'Canceled'

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default=OrderStatus.NEW, choices=OrderStatus.choices)

    ranked_objects = OrderRang()
    objects = models.Manager()

    def get_items(self) -> models.QuerySet:
        return self.items.all()


class OrderItem(BaseCartItem):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE)

    @hook(AFTER_DELETE)
    def remove_item(self):
        self.order.recalculate()

    @hook(BEFORE_SAVE)
    def set_amount(self):
        self.amount = self.product.price * self.quantity

    @hook(AFTER_SAVE)
    def recalculate_cart(self):
        self.order.recalculate()
