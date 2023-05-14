from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ["date_edited", "tour"]

    rating = forms.IntegerField(min_value=0, max_value=5)
  
  

