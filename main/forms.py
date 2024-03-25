from django import forms
from .models import *

#movie add form
class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ('name', 'director', 'cast','description', 'release_date', 'image')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("comment", "rating")

