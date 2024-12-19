from django import forms
from .models import Review, Profile


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['favorite_genre', 'favorite_author']
        widgets = {
            'favorite_genre': forms.TextInput(attrs={'placeholder': 'Enter your favorite genre'}),
            'favorite_author': forms.TextInput(attrs={'placeholder': 'Enter your favorite author(s)'}),
        }

class ReviewForm(forms.ModelForm):
    book_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Enter the full book name'})
    )

    author_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Enter the author name'})
    )

    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={'placeholder': 'Rate this book (1-5)'})
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Write your review here...'})
    )

    class Meta:
        model = Review
        fields = ['book_name', 'author_name', 'rating', 'comment']
