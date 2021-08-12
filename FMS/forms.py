from django import forms
from .models import Image

class Image_form(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']
    