from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Book, Review
from .serializers import BookSerializer, ReviewSerializer
from django.shortcuts import render

class BookListView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class ReviewListView(APIView):
    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

def index(request):
    return render(request, 'index.html')

def home_view(request):
    return render(request, 'home.html')

def login_view(request):
    return render(request, 'login.html')

def profile_view(request):
    return render(request, 'profile.html')

def reviews_view(request):
    return render(request, 'reviews.html')

def bookshelf_view(request):
    return render(request, 'bookshelf.html')