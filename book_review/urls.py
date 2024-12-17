from django.urls import path
from .views import BookListView, ReviewListView
from . import views

urlpatterns = [
    path('api/books/', BookListView.as_view(), name='book-list'),
    path('api/reviews/', ReviewListView.as_view(), name='review-list'),
    path('', views.home_view, name='home'),  # Home page
    path('login/', views.login_view, name='login'),  # Login page
    path('profile/', views.profile_view, name='profile'),  # Profile page
    path('reviews/', views.reviews_view, name='reviews'),  # Reviews page
    path('bookshelf/', views.bookshelf_view, name='bookshelf'),  # Bookshelf page

]
