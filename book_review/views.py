from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile, Book, Review, Bookshelf
from .serializers import BookSerializer, ReviewSerializer
from django.views.generic import TemplateView
from django.shortcuts import render
import requests
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
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
from .forms import ReviewForm, ProfileUpdateForm
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db import models
import os
from dotenv import load_dotenv
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.http import JsonResponse



load_dotenv()


my_api_key = os.getenv('API_KEY')

class BookListView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


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


class SetPreferencesView(LoginRequiredMixin, FormView):
    template_name = 'preferences.html'
    form_class = ProfileUpdateForm
    success_url = '/'  # Redirect to home page after saving preferences

    def form_valid(self, form):
        # Save user preferences
        profile = form.save(commit=False)
        profile.user = self.request.user
        profile.save()
        return super().form_valid(form)

# Login View
class LoginView(FormView):
    template_name = 'login.html'
    success_url = reverse_lazy('home')  # Default redirect to home after login

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

            # Check if the user has preferences set
            if not hasattr(user, 'profile') or not user.profile.favorite_genre:
                # Redirect to preferences form if the user is new or preferences are not set
                return redirect('set_preferences')
            
            # Redirect to home if preferences are already set
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

        # Fetch Google Books API key
        google_books_api_key = my_api_key

        # Fetch new releases from Google Books API
        try:
            google_books_url = f'https://www.googleapis.com/books/v1/volumes?q=new+releases&key={google_books_api_key}'
            response = requests.get(google_books_url)
            response.raise_for_status()
            books_data = response.json()

            # Extract book details
            new_releases = [
                {
                    'title': item['volumeInfo'].get('title', 'No Title'),
                    'author': ', '.join(item['volumeInfo'].get('authors', ['Unknown Author'])),
                    'description': item['volumeInfo'].get('description', 'No description available'),
                    'cover_image': item['volumeInfo'].get('imageLinks', {}).get('thumbnail', ''),
                }
                for item in books_data.get('items', [])
            ]
        except requests.exceptions.RequestException:
            new_releases = []

        context['new_releases'] = new_releases

        # Get the logged-in user's profile
        if self.request.user.is_authenticated:
            profile = get_object_or_404(Profile, user=self.request.user)

            # Fetch user reviews
            user_reviews = Review.objects.filter(user=self.request.user)

            # If no reviews, use profile preferences for recommendations
            if not user_reviews.exists():
                search_query = f"subject:{profile.favorite_genre} inauthor:{profile.favorite_author}"
            else:
                # Get the latest rated book
                latest_review = user_reviews.order_by('-created_at').first()
                latest_book = latest_review.book
                user_rating = latest_review.rating

                # Use the user's rating to adjust the search query
                search_query = (
                    f"inauthor:{latest_book.author}" if user_rating >= 3
                    else f"subject:-{latest_book.genre}"
                )

            # Fetch recommendations from Google Books API
            try:
                google_books_url = f'https://www.googleapis.com/books/v1/volumes?q={search_query}&key={google_books_api_key}'
                response = requests.get(google_books_url)
                response.raise_for_status()
                books_data = response.json()

                recommended_books = [
                    {
                        'title': item['volumeInfo'].get('title', 'No Title'),
                        'author': ', '.join(item['volumeInfo'].get('authors', ['Unknown Author'])),
                        'description': item['volumeInfo'].get('description', 'No description available'),
                        'cover_image': item['volumeInfo'].get('imageLinks', {}).get('thumbnail', ''),
                    }
                    for item in books_data.get('items', [])
                ]
            except requests.exceptions.RequestException:
                recommended_books = []

            context['recommended_books'] = recommended_books
        else:
            # No user logged in
            context['recommended_books'] = None

        # Add fallback message if no recommendations
        if not context['recommended_books']:
            context['no_ratings_message'] = "No recommendations available. Start rating books to get personalized suggestions!"

        return context

class ProfileView(TemplateView):
    template_name = 'profile.html'

class ReviewsView(View):
    def get(self, request):
        reviews = Review.objects.filter(user=request.user)  # Fetch all reviews
        return render(request, 'reviews.html', {'reviews': reviews, 'message': 'No reviews yet.'})

class NewReviewView(View):
    def get(self, request):
        form = ReviewForm()  # Create a blank form
        return render(request, 'new_review.html', {'form': form})

    def post(self, request):
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Get or create the book based on the book name
            book_name = form.cleaned_data['book_name']
            book, created = Book.objects.get_or_create(title=book_name)

            # Save the review with the book
            review = form.save(commit=False)
            review.book = book
            review.user = request.user  # Associate the review with the logged-in user
            review.save()

            return redirect('reviews')  # Redirect back to the reviews page
        return render(request, 'new_review.html', {'form': form})
    

class BookshelfView(LoginRequiredMixin, View):
    def get(self, request):
        # Get the bookshelf of the logged-in user
        bookshelf = Bookshelf.objects.filter(user=request.user).first()
        books = bookshelf.books.all() if bookshelf else []
        return render(request, 'bookshelf.html', {'bookshelf': books})

    def post(self, request):
        # Handle adding a book to the bookshelf
        book_id = request.POST.get('book_id')  # Get book_id from form data
        if not book_id:
            return JsonResponse({'message': 'Book ID is required'}, status=400)

        try:
            book = Book.objects.get(id=book_id)
            bookshelf, created = Bookshelf.objects.get_or_create(user=request.user)
            bookshelf.books.add(book)
            return JsonResponse({'message': 'Book added to bookshelf successfully'})
        except Book.DoesNotExist:
            return JsonResponse({'message': 'Book not found'}, status=404)


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