from django.contrib import admin
from .models import Order, User, OrderBook, Review, Book


class OrderBookInline(admin.TabularInline):
    model = OrderBook
    # extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderBookInline]


# Register your models here.
admin.site.register(Order, OrderAdmin)
admin.site.register(User)
admin.site.register(Review)
admin.site.register(Book)
