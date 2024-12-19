from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=1, max_value=5, widget=forms.NumberInput(attrs={'placeholder': 'Rate this book (1-5)'}))
    comment = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Write your review here...'}))

    class Meta:
        model = Review
        fields = ['rating', 'comment']
