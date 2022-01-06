from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import re

# Create your models here.

class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})

	def get_youtube_urls(self):
		urls = []
		youtube_regex = (
			r'(https?://)?(www\.)?'
			'(youtube)\.(com)/'
			'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

		matches = re.findall(youtube_regex, self.content)

		for url in matches:
			urls.append(url[5])

		return urls

class PostImage(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='post_pics', blank=True, null=True)

	def __str__(self):
		return self.post.title

	def save(self, *args, **kwargs):
		if PostImage.objects.filter(post=self.post).count() >= 7:
			return
		else:
			super(PostImage, self).save(*args, **kwargs)

	# @property
	# def image_url(self):
	# 	"""
	# 	Return self.photo.url if self.photo is not None, 
	# 	'url' exist and has a value, else, return None.
	# 	"""
	# 	if self.image:
	# 	    return getattr(self.image, 'url', None)
	# 	return None
