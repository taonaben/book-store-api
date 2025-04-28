from django.db import transaction
from rest_framework import serializers
from .models import Book, Order, OrderBook, Review, User, Comment


class UserSerializer(serializers.ModelSerializer):

    # id = serializers.UUIDField(read_only=True)
    class Meta:
        model = User 
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
           
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ReviewSerializer(serializers.ModelSerializer):

    comment_count = serializers.SerializerMethodField(method_name="get_comment_count")

    def get_comment_count(self, obj):
        return obj.comments.count()

    class Meta:
        model = Review
        fields = (
            "id",
            "rating",
            "review_text",
            "upvotes",
            # "comments",
            "comment_count",
            "created_at",
        )
        extra_kwargs = {
            "book": {"write_only": True},
        }


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "comment_text",
            "created_at",
        )
        extra_kwargs = {
            "review": {"write_only": True},
        }


class BookSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many=True, read_only=True)
    review_count = serializers.SerializerMethodField(method_name="get_review_count")

    def get_review_count(self, obj):
        return obj.reviews.count()

    class Meta:
        model = Book
        fields = (
            "id",
            "name",
            "author",
            "description",
            "published_date",
            "publisher",
            "genre",
            "language",
            "number_of_pages",
            "age_rating",
            "review_count",
            "stock",
            "price",
            "discount",
            "file_link",
            "image",
        )

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value


class OrderBookSerializer(serializers.ModelSerializer):
    book_name = serializers.CharField(source="book.name", read_only=True)
    book_author = serializers.CharField(source="book.author", read_only=True)
    book_price = serializers.DecimalField(
        source="book.price",
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )
    # quantity = serializers.IntegerField()

    class Meta:
        model = OrderBook
        fields = (
            "book_name",
            "book_author",
            "book_price",
            "quantity",
            "item_subtotal",
        )
        # extra_kwargs = {
        #     "book": {"write_only": True},
        # }


class OrderCreateSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderBook
            fields = ("book", "quantity")

    order_id = serializers.UUIDField(read_only=True)
    books = OrderItemCreateSerializer(many=True, required=False)

    def update(self, instance, validated_data):

        order_book_data = validated_data.pop("books")

        with transaction.atomic():
            instance = super().update(instance, validated_data)

            if order_book_data is not None:
                instance.books.all().delete()
                for order_book in order_book_data:
                    OrderBook.objects.create(order=instance, **order_book)

        return instance

    def create(self, validated_data):
        order_book_data = validated_data.pop("books")

        with transaction.atomic():
            order = Order.objects.create(**validated_data)

            for book in order_book_data:
                OrderBook.objects.create(order=order, **book)

        return order

    class Meta:
        model = Order
        fields = (
            "order_id",
            "user",
            "status",
            "books",
        )
        extra_kwargs = {
            "user": {"read_only": True},
        }


class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)
    orderbook_set = OrderBookSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name="total")
    total_items = serializers.SerializerMethodField(method_name="items")

    def total(self, obj):

        order_books = obj.orderbook_set.all()
        return sum([order_book.item_subtotal for order_book in order_books])

    def items(self, obj):
        order_books = obj.orderbook_set.all()
        return sum([order_book.quantity for order_book in order_books])

    class Meta:
        model = Order
        fields = (
            "order_id",
            "user",
            "status",
            "orderbook_set",
            "total_items",
            "total_price",
            "created_at",
        )


###


class BookInfoSerializer(serializers.Serializer):
    books = BookSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()
