from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


urlpatterns = [
    path("books/", views.BookListCreateApiView.as_view()),
    path("books/info/", views.BookInfoAPIView.as_view()),
    path("books/<uuid:book_id>/", views.BookDetailApiView.as_view()),
    path("users/", views.UserListView.as_view()),
    path(
        "reviews/<uuid:book_id>/",
        views.ReviewListCreateAPIView.as_view(),
        name="review-list-create",
    ),
    path(
        "reviews/<uuid:book_id>/<uuid:id>/",
        views.ReviewDetailAPIView.as_view(),
        name="review-detail",
    ),
    path(
        "comments/<uuid:review_id>/",
        views.CommentListCreateAPIView.as_view(),
        name="comment-list-create",
    ),
    path(
        "comments/<uuid:review_id>/<uuid:id>/",
        views.CommentDetailAPIView.as_view(),
        name="comment-detail",
    )
]

router.register(
    "orders",
    views.OrderViewSet,
)

urlpatterns += router.urls
