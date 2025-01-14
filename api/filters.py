from api.models import Book, Order
import django_filters

from rest_framework import filters

class InStockFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)

class BookFilter(django_filters.FilterSet):
    class Meta:
        model = Book
        fields = {
            "name": ["iexact", "icontains"],
            "author": ["iexact", "icontains"],
            "price": ["exact", "lt", "gt", "range"],
        }

class OrderFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(field_name='created_at__date')
    class Meta:
        model = Order
        fields = {
            "status": ["exact"],
            "created_at": ["date", "gt", "lt", "range"],
        }