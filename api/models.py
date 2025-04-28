import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    pass




class Book(models.Model):
    class LanguageChoices(models.TextChoices):
        ENGLISH = "ENGLISH", "English"
        GERMAN = "GERMAN", "German"
        SHONA = "SHONA", "Shona"
        FRENCH = "FRENCH", "French"

    class AgeRatingChoices(models.TextChoices):
        CHILDREN = "10+", "CHILDREN"
        TEEN = "16+", "TEEN"
        ADULT = "18+", "ADULT"

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    publisher = models.CharField(max_length=200)
    genre = models.CharField(max_length=200, default='')
    language = models.CharField(
        max_length=200, choices=LanguageChoices.choices, default=LanguageChoices.ENGLISH
    )
    number_of_pages = models.PositiveIntegerField(default=0)
    age_rating = models.CharField(
        max_length=10, choices=AgeRatingChoices.choices, default=AgeRatingChoices.TEEN
    )
    stock = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discount = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    file_link = models.URLField(null=True, blank=True)
    image = models.ImageField(upload_to="books/", null=True, blank=True)

    @property
    def in_stock(self):
        return self.stock > 0

    def __str__(self):
        return self.name



class Review(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews", null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    upvotes = models.PositiveIntegerField(default=0)
    
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating} stars by {self.user.username} for {self.book.name}"


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "PENDING", "Pending"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    order_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING
    )
    books = models.ManyToManyField(Book, through="OrderBook", related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.order_id} by {self.user.username}"


class OrderBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="orderbook_set"
    )
    quantity = models.PositiveIntegerField()

    @property
    def item_subtotal(self):
        return self.quantity * self.book.price

    def __str__(self):
        return f"{self.quantity} x {self.book.name} in order #{self.order.order_id}"
