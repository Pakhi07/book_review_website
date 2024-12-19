from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Book, Review
from .serializers import BookSerializer, ReviewSerializer
from django.views.generic import TemplateView
from django.shortcuts import render
import requests
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from .models import Rating
from django import forms
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from rest_framework_simplejwt.tokens import RefreshToken
from .forms import ReviewForm



my_api_key = "AIzaSyALS7QGQhjpmqrfJ9GX52Saj0tVqEU_Qyc"

class BookListView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

# class ReviewListView(APIView):
#     def post(self, request):
#         serializer = ReviewSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)

# def index(request):
#     return render(request, 'index.html')

# def home_view(request):
#     return render(request, 'home.html')

# def login_view(request):
#     return render(request, 'login.html')

# def profile_view(request):
#     return render(request, 'profile.html')

# def reviews_view(request):
#     return render(request, 'reviews.html')

# def bookshelf_view(request):
#     return render(request, 'bookshelf.html')

# def browse_view(request):
#     return render(request, 'browse.html')

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')  # Redirect to login after registration

    def form_valid(self, form):
        user = form.save()  # Save the new user
        user.is_staff = True  # Mark the user as staff to appear in admin
        user.save()  # Save the updated user
        messages.success(self.request, 'Your account has been created! You can now log in.')
        return super().form_valid(form)


# Login View
class LoginView(FormView):
    template_name = 'login.html'
    success_url = reverse_lazy('home')  # Redirect to home after login

    # Custom form to handle username and password
    class LoginForm(forms.Form):
        username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
            'placeholder': 'Enter your username',
            'class': 'form-control'
        }))
        password = forms.CharField(widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'class': 'form-control'
        }))

    form_class = LoginForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, 'You have successfully logged in!')
            return super().form_valid(form)
        else:
            form.add_error(None, 'Invalid username or password.')
            return self.form_invalid(form)
        

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have successfully logged out!')
        return redirect('login')


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        google_books_api_key = my_api_key  # Replace with your API key
        google_books_url = f'https://www.googleapis.com/books/v1/volumes?q=new+releases&key={google_books_api_key}'
        response = requests.get(google_books_url)
        books_data = response.json()

        # Extract book details from the API response
        new_releases = []
        if 'items' in books_data:
            for item in books_data['items']:
                book = item['volumeInfo']
                new_releases.append({
                    'title': book.get('title', 'No Title'),
                    'author': ', '.join(book.get('authors', ['Unknown Author'])),
                    'description': book.get('description', 'No description available'),
                    'cover_image': book.get('imageLinks', {}).get('thumbnail', ''),
                })

        context['new_releases'] = new_releases

        # Fetch new releases
        # context['new_releases'] = Book.objects.all()[:5]  # Example: Fetch the first 5 books

        # Fetch user ratings
        user_ratings = Rating.objects.filter(user=self.request.user)
        
        # If the user has no ratings, set a flag and return early
        if user_ratings.count() == 0:
            context['recommended_books'] = None  # No recommendations
            context['no_ratings_message'] = "No recommendations available. Start rating books to get personalized suggestions!"
            return context

        # If the user has ratings, proceed with recommendation logic
        ratings_df = pd.DataFrame(list(user_ratings.values('user_id', 'book_id', 'rating')))

        # Create a pivot table of users and their ratings
        ratings_pivot = ratings_df.pivot(index='user_id', columns='book_id', values='rating').fillna(0)

        # Compute similarity between users
        user_similarity = cosine_similarity(ratings_pivot)
        user_similarity_df = pd.DataFrame(user_similarity, index=ratings_pivot.index, columns=ratings_pivot.index)

        # Get the current user's similarity scores
        current_user = self.request.user
        if current_user.id in user_similarity_df.index:
            similar_users = user_similarity_df[current_user.id].sort_values(ascending=False)

            # Recommend books rated highly by similar users
            similar_user_ids = similar_users.index[1:6]  # Top 5 similar users
            recommended_books = Rating.objects.filter(
                user_id__in=similar_user_ids, rating__gte=4
            ).values_list('book', flat=True)
            context['recommended_books'] = Book.objects.filter(id__in=recommended_books).distinct()
        else:
            context['recommended_books'] = Book.objects.none()

        return context

class ProfileView(TemplateView):
    template_name = 'profile.html'

class ReviewsView(TemplateView):
    template_name = 'reviews.html'

    def get(self, request, *args, **kwargs):
        # Get the book from the URL or pass an error message
        book_id = self.kwargs.get('book_id')
        book = Book.objects.get(id=book_id)
        
        # Get all reviews for this book
        reviews = Review.objects.filter(book=book)

        # If the user has rated the book, fetch their rating
        user_rating = Rating.objects.filter(user=request.user, book=book).first()

        # Pass reviews and the user's rating to the template
        return render(request, self.template_name, {
            'book': book,
            'reviews': reviews,
            'user_rating': user_rating,
            'form': ReviewForm(),
        })

    def post(self, request, *args, **kwargs):
        # Handle form submission for a new review
        book_id = self.kwargs.get('book_id')
        book = Book.objects.get(id=book_id)

        # Handle review form submission
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Save the review
            review = form.save(commit=False)
            review.user = request.user
            review.book = book
            review.save()

            # Save the rating
            rating = Rating.objects.filter(user=request.user, book=book).first()
            if rating:
                rating.rating = form.cleaned_data['rating']
                rating.save()
            else:
                Rating.objects.create(user=request.user, book=book, rating=form.cleaned_data['rating'])

            messages.success(request, 'Your review has been added!')
            return redirect('reviews', book_id=book.id)

        return render(request, self.template_name, {'form': form, 'book': book})

class BookshelfView(TemplateView):
    template_name = 'bookshelf.html'

class BrowseView(TemplateView):
    template_name = 'browse.html'

    def get(self, request):
        # Get search parameters from the request
        query = request.GET.get('q', '')  # Book name
        genre = request.GET.get('genre', '')  # Book genre

        # Google Books API setup
        api_url = "https://www.googleapis.com/books/v1/volumes"
        api_key = my_api_key  # Replace with your API key

        # Build the API query
        params = {
            'q': f"{query}+subject:{genre}" if genre else query,
            'key': api_key,
            'maxResults': 20
        }

        # Fetch data from the API
        response = requests.get(api_url, params=params)
        books = response.json().get('items', []) if response.status_code == 200 else []

        # Pass the books data to the template
        return render(request, self.template_name, {'books': books})