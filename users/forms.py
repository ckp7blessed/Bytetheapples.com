from django import forms
from django.forms.widgets import ClearableFileInput, FileInput
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from . models import Profile

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()
	class Meta:
		model = User 
		fields = ['username', 'email', 'first_name', 'last_name','password1', 'password2']

class CustomAuthForm(AuthenticationForm):
	class Meta:
		model = User 
		fields = ['username', 'password']
	def __init__(self, *args, **kwargs):
		super(CustomAuthForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username or Email'})
		self.fields['username'].label = False
		self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}) 
		self.fields['password'].label = False

class UserUpdateForm(forms.ModelForm):
	username = forms.CharField(max_length=20)
	class Meta:
		model = User 
		fields = ['username', 'first_name', 'last_name']

	def __init__(self, *args, **kwargs):
		super(UserUpdateForm, self).__init__(*args, **kwargs)
		self.fields['username'].help_text = 'Required. 20 characters or fewer. Letters, digits and @/./+/-/_ only. Must be unique.'

class ProfileUpdateForm(forms.ModelForm):
	image = forms.ImageField(label='Profile Picture', required=False, widget=FileInput)
	background_image = forms.ImageField(label='Background Image', required=False, widget=FileInput)
	class Meta:
		model = Profile 
		fields = '__all__'
		exclude = ['user', 'followers']
	def __init__(self, *args, **kwargs):
		super(ProfileUpdateForm, self).__init__(*args, **kwargs)
		self.fields['bio'].widget = forms.Textarea(attrs={'rows': 4, 'cols': 25})



