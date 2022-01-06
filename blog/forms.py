from django import forms
from .models import Post, PostImage
from django.forms import inlineformset_factory
from django.forms.widgets import ClearableFileInput


class ImageForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = PostImage
        fields = ['image']


ImageFormSet = inlineformset_factory(Post, PostImage, form=ImageForm, extra=1)