from django.urls import path
from . import views

urlpatterns = [
    path('api/books/', views.BookListView.as_view(), name='book-list'),
    # path('api/reviews/', views.ReviewListView.as_view(), name='review-list'),
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('reviews/', views.ReviewsView.as_view(), name='reviews'),
    path('reviews/new/', views.NewReviewView.as_view(), name='new_review'),
    path('bookshelf/', views.BookshelfView.as_view(), name='bookshelf'),
    path('browse/', views.BrowseView.as_view(), name='browse'),
    
]
