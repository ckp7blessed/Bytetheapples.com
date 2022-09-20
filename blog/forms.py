from django import forms
from .models import Post, PostImage, Category, Comment, MessageModel
from django.forms import inlineformset_factory
from django.forms.widgets import ClearableFileInput


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Add images', required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = PostImage
        fields = ['image']

ImageFormSet = inlineformset_factory(Post, PostImage, form=ImageForm, extra=1, can_delete=False)

class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label='', 
                            widget=
                            forms.Textarea(
                                attrs={'placeholder': 'Write your reply \nMax 300 characters.', 
                                'rows': 1, 'cols': 25}))
    class Meta:
        model = Comment 
        fields = ['body']

class ThreadForm(forms.Form):
    username = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder': '@'}))

class MessageForm(forms.ModelForm):
    body = forms.CharField(label='', max_length=1000)

    image = forms.ImageField(label='Add an image', required=False)

    class Meta:
        model = MessageModel
        fields = ['body', 'image']