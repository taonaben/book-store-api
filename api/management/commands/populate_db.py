import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import lorem_ipsum
from api.models import User, Book, Order, OrderBook

class Command(BaseCommand):
    help = 'Creates application data'

    def handle(self, *args, **kwargs):
        # get or create superuser
        user = User.objects.filter(username='admin').first()
        if not user:
            user = User.objects.create_superuser(username='admin', password='test')

        # create books - name, author, description, price, stock
        books = [
            Book(
                name="A Scanner Darkly",
                author="Philip K. Dick",
                description=lorem_ipsum.paragraph(),
                published_date="1977-01-01",
                publisher="Doubleday",
                genre="Science fiction",
                language="English",
                number_of_pages=272,
                age_rating="TEEN",
                stock=4,
                price=Decimal('9.99'),
                discount=Decimal('0.00'),
                file_link="https://example.com/a-scanner-darkly.epub"
            ),
            Book(
                name="1984",
                author="George Orwell",
                description=lorem_ipsum.paragraph(),
                published_date="1949-06-08",
                publisher="Secker and Warburg",
                genre="Dystopian",
                language="English",
                number_of_pages=328,
                age_rating="TEEN",
                stock=6,
                price=Decimal('8.99'),
                discount=Decimal('0.00'),
                file_link="https://example.com/1984.epub"
            ),
            Book(
                name="To Kill a Mockingbird",
                author="Harper Lee",
                description=lorem_ipsum.paragraph(),
                published_date="1960-07-11",
                publisher="J. B. Lippincott & Co.",
                genre="Southern Gothic",
                language="English",
                number_of_pages=281,
                age_rating="TEEN",
                stock=11,
                price=Decimal('7.99'),
                discount=Decimal('0.00'),
                file_link="https://example.com/to-kill-a-mockingbird.epub"
            ),
            Book(
                name="The Great Gatsby",
                author="F. Scott Fitzgerald",
                description=lorem_ipsum.paragraph(),
                published_date="1925-04-10",
                publisher="Charles Scribner\'s Sons",
                genre="Novel",
                language="English",
                number_of_pages=180,
                age_rating="TEEN",
                stock=2,
                price=Decimal('10.99'),
                discount=Decimal('0.00'),
                file_link="https://example.com/the-great-gatsby.epub"
            ),
            Book(
                name="Moby Dick",
                author="Herman Melville",
                description=lorem_ipsum.paragraph(),
                published_date="1851-11-14",
                publisher="Harper & Brothers",
                genre="Epic",
                language="English",
                number_of_pages=640,
                age_rating="TEEN",
                stock=4,
                price=Decimal('6.99'),
                discount=Decimal('0.00'),
                file_link="https://example.com/moby-dick.epub"
            ),
            Book(
                name="War and Peace",
                author="Leo Tolstoy",
                description=lorem_ipsum.paragraph(),
                published_date="1869-01-01",
                publisher="The Russian Messenger",
                genre="Historical fiction",
                language="Russian",
                number_of_pages=1225,
                age_rating="TEEN",
                stock=0,
                price=Decimal('12.99'),
                discount=Decimal('0.00'),
                file_link="https://example.com/war-and-peace.epub"
            ),
            Book(
                name="Pride and Prejudice",
                author="Jane Austen",
                description=lorem_ipsum.paragraph(),
                published_date="1813-01-28",
                publisher="T. Egerton",
                genre="Romance",
                language="English",
                number_of_pages=320,
                age_rating="TEEN",
                stock=10,
                price=Decimal('5.99'),
                discount=Decimal('0.00'),
                file_link="https://example.com/pride-and-prejudice.epub"
            ),
            Book(
                name="The Catcher in the Rye",
                author="J.D. Salinger",
                description=lorem_ipsum.paragraph(),
                published_date="1951-07-16",
                publisher="Little, Brown and Company",
                genre="Coming-of-age",
                language="English",
                number_of_pages=272,
                age_rating="TEEN",
                stock=7,
                price=Decimal('8.99'),
                discount=Decimal('0.00'),
                file_link="https://example.com/the-catcher-in-the-rye.epub"
            ),
            Book(
                name="The Hitchhiker\'s Guide to the Galaxy",
                author="Douglas Adams",
                description=lorem_ipsum.paragraph(),
                published_date="1979-10-12",
                publisher="Pan Books",
                genre="Science fiction",
                language="English",
                number_of_pages=320,
                age_rating="TEEN",
                stock=1,
                price=Decimal('9.99'),
                discount=Decimal('0.00'),
                file_link="https://example.com/the-hitchhikers-guide-to-the-galaxy.epub"
            ),
            Book(
                name="The Picture of Dorian Gray",
                author="Oscar Wilde",
                description=lorem_ipsum.paragraph(),
                published_date="1890-07-01",
                publisher="Lippincott\'s Monthly Magazine",
                genre="Philosophical novel",
                language="English",
                number_of_pages=176,
                age_rating="TEEN",
                stock=8,
                price=Decimal('7.99'),
                discount=Decimal('0.00'),
                file_link="https://example.com/the-picture-of-dorian-gray.epub"
            ),
            Book(
                name="Frankenstein",
                author="Mary Shelley",
                description=lorem_ipsum.paragraph(),
                published_date="1818-01-01",
                publisher="Lackington, Hughes, Harding, Mavor, & Jones",
                genre="Gothic novel",
                language="English",
                number_of_pages=272,
                age_rating="TEEN",
                stock=5,
                price=Decimal('9.99'),
                discount=Decimal('0.00'),
                file_link="https://example.com/frankenstein.epub"
            ),
            Book(
                name="The Count of Monte Cristo",
                author="Alexandre Dumas",
                description=lorem_ipsum.paragraph(),
                published_date="1844-01-01",
                publisher="Pierre-Jules Hetzel",
                genre="Adventure",
                language="French",
                number_of_pages=1176,
                age_rating="TEEN",
                stock=3,
                price=Decimal('8.99'),
                discount=Decimal('0.00'),
                file_link="https://example.com/the-count-of-monte-cristo.epub"
            ),
            Book(
                name="The Adventures of Huckleberry Finn",
                author="Mark Twain",
                description=lorem_ipsum.paragraph(),
                published_date="1884-02-18",
                publisher="Chatto and Windus",
                genre="Satire",
                language="English",
                number_of_pages=366,
                age_rating="TEEN",
                stock=2,
                price=Decimal('6.99'),
                discount=Decimal('0.00'),
                file_link="https://example.com/the-adventures-of-huckleberry-finn.epub"
            ),
            Book(
                name="The Adventures of Tom Sawyer",
                author="Mark Twain",
                description=lorem_ipsum.paragraph(),
                published_date="1876-06-01",
                publisher="American Publishing Company",
                genre="Satire",
                language="English",
                number_of_pages=224,
                age_rating="TEEN",
                stock=3,
                price=Decimal('7.99'),
                discount=Decimal('0.00'),
                file_link="https://example.com/the-adventures-of-tom-sawyer.epub"
            ),
            Book(
                name="The Lord of the Rings: The Fellowship of the Ring",
                author="J.R.R. Tolkien",
                description=lorem_ipsum.paragraph(),
                published_date="1954-07-29",
                publisher="Allen & Unwin",
                genre="Fantasy",
                language="English",
                number_of_pages=423,
                age_rating="TEEN",
                stock=0,
                price=Decimal('12.99'),
                discount=Decimal('0.00'),
                file_link="https://example.com/the-lord-of-the-rings-the-fellowship-of-the-ring.epub"
            ),
        ]

        # create books & re-fetch from DB
        Book.objects.bulk_create(books)
        books = Book.objects.all()


        # create some dummy orders tied to the superuser
        for _ in range(3):
            # create an Order with 2 order items
            order = Order.objects.create(user=user)
            for book in random.sample(list(books), 2):
                OrderBook.objects.create(
                    order=order, book=book, quantity=random.randint(1,3)
                )