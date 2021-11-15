from django.db import models


class Topping(models.Model):
    name = models.CharField(max_length=200, default='')
    size = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.name


class Pizza(models.Model):
    name = models.CharField(max_length=200)
    toppings = models.ManyToManyField(Topping, blank=True)

    def __str__(self):
        return self.name
