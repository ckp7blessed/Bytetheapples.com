from django import forms
from .models import Post, PostImage, Category, Comment
from django.forms import inlineformset_factory
from django.forms.widgets import ClearableFileInput

# cat_choice = Category.objects.all()

class ImageForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = PostImage
        fields = ['image']

# class CatForm(forms.ModelForm):
#     category = forms.Select(choices=cat_choice)

#     class Meta:
#         model = Post
#         fields = ['category']


ImageFormSet = inlineformset_factory(Post, PostImage, form=ImageForm, extra=1)
# CatFormSet = inlineformset_factory(Category, Post, form=CatForm)

class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label='', 
                            widget=forms.TextInput(attrs={'placeholder': 'Add a comment...'}))
    class Meta:
        model = Comment 
        fields = ('body', )