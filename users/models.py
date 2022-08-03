from django.db import models
from django.contrib.auth.models import User
from PIL import Image 

# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')
	background_image = models.ImageField(upload_to='profile_background_pics', blank=True, null=True,)
	bio = models.CharField(max_length=200, help_text="200 characters or less")
	location = models.CharField(max_length=50, default="n/a", help_text="City, State, Country")
	website_url = models.CharField(max_length=75, blank=True, null=True)
	linkedin_url = models.CharField(max_length=75, blank=True, null=True)
	github_url = models.CharField(max_length=75, blank=True, null=True)
	stackoverflow_url = models.CharField(max_length=75, blank=True, null=True)
	facebook_url = models.CharField(max_length=75, blank=True, null=True)
	instagram_url = models.CharField(max_length=75, blank=True, null=True)
	twitter_url = models.CharField(max_length=75, blank=True, null=True)
	youtube_url = models.CharField(max_length=75, blank=True, null=True)
	show_email = models.BooleanField(default=True, verbose_name="Show email in profile")
	followers = models.ManyToManyField(User, blank=True, related_name="followers")

	def __str__(self):
		return f"{self.user.username}"

#--- profile picture resizing. update to AWS Lambda for production ---#
	# def save(self, *args, **kwargs):
	# 	super().save(*args, **kwargs)
	# 	img = Image.open(self.image.path)
	# 	if img.height > 300 or img.width > 300:
	# 		output_size = (300, 300)
	# 		img.thumbnail(output_size)
	# 		img.save(self.image.path)