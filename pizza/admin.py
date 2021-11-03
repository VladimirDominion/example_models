from django.contrib import admin

from .models import Pizza, Topping


@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    filter_horizontal = ('toppings',)

