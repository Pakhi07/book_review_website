from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    book_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Enter the full book name'})
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
        fields = ['book_name', 'rating', 'comment']
