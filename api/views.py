from django.db.models import Max
from django.shortcuts import get_list_or_404, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from api.filters import InStockFilterBackend, OrderFilter, BookFilter
from api.models import Order, Book, OrderBook, User, Review
from api.serializers import (
    OrderCreateSerializer,
    OrderSerializer,
    BookSerializer,
    BookInfoSerializer,
    UserSerializer,
    ReviewSerializer,
    CommentSerializer,
)


##get all products or create a new product
class BookListCreateApiView(generics.ListCreateAPIView):
    queryset = Book.objects.order_by("pk")
    serializer_class = BookSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        InStockFilterBackend,
    ]
    filterset_class = BookFilter
    search_fields = [
        "name",
        "author",
        "stock",
        "description",
        "publisher",
        "published_date",
        "genre",
        "language",
        "number_of_pages",
        "age_rating",
        "price",
    ]
    pagination_class = LimitOffsetPagination

    def get_permissions(self):
        self.permission_classes = [permissions.AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()


## get a single book


class BookDetailApiView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # lookup_field = "pk"
    lookup_url_kwarg = "book_id"

    def get_permissions(self):
        self.permission_classes = [permissions.AllowAny]
        if self.request.method == ["PUT", "DELETE", "PATCH"]:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("orderbook_set__book").order_by("pk")

    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return OrderCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs


class BookInfoAPIView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookInfoSerializer(
            {
                "books": books,
                "count": books.count(),
                "max_price": books.aggregate(Max("price"))["price__max"],
            }
        )
        return Response({"books": serializer.data})


class ReviewListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        book_id = self.kwargs["book_id"]
        book = get_object_or_404(Book, id=book_id)
        return book.reviews.all()

    def perform_create(self, serializer):
        book_id = self.kwargs["book_id"]
        book = get_object_or_404(Book, id=book_id)
        serializer.save(book=book, user=self.request.user)


class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    lookup_field = "id"
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        book_id = self.kwargs["book_id"]
        book = get_object_or_404(Book, id=book_id)
        return book.reviews.all()


class CommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review_id = self.kwargs["review_id"]
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs["review_id"]
        review = get_object_or_404(Review, id=review_id)
        serializer.save(review=review, user=self.request.user)


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    lookup_field = "id"

    def get_queryset(self):
        review_id = self.kwargs["review_id"]
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return super().get_queryset().filter(is_staff=False)


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(is_staff=False)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "id"


