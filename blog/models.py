from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from users.models import Profile
from django.urls import reverse
import re


class Category(models.Model):
	category_name = models.CharField(max_length=50, default='general coding', verbose_name="Categories")

	def __str__(self):
		return self.category_name 

	def get_absolute_url(self):
		return reverse('blog-home')

class Post(models.Model):
	title = models.CharField(max_length=100, help_text="100 characters or less")
	content = models.TextField(max_length=3000, help_text="3k characters or less")
	category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	liked = models.ManyToManyField(Profile, blank=True, related_name='likes')
	ip_address = models.CharField(max_length=25, default='00.000.000.000', blank=True, null=True)

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

	def num_likes(self):
		return self.liked.all().count()
	num_likes.short_description = 'Total Likes'

	def num_comments(self):
		return self.comment_set.all().count()

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

LIKE_CHOICES = (
	('Like', 'Like'),
	('Unlike', 'Unlike'),
)

class Like(models.Model):
	user = models.ForeignKey(Profile, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	value = models.CharField(choices=LIKE_CHOICES, max_length=8)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)
	ip_address = models.CharField(max_length=25, default='00.000.000.000', blank=True, null=True)

	def __str__(self):
		return f"{self.user}-{self.post}-{self.value}"

class Comment(models.Model):
	user = models.ForeignKey(Profile, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	body = models.TextField(max_length=300)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)
	liked = models.ManyToManyField(Profile, blank=True, related_name='com_likes')
	parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
	ip_address = models.CharField(max_length=25, default='00.000.000.000', blank=True, null=True)

	def __str__(self):
		return f"Comment:{self.user}-{self.post}-{self.id}"

	def post_id(self):
		return self.post.id

	def post_author(self):
		return self.post.author

	def num_likes(self):
		return self.liked.all().count()

	def num_children(self):
		return Comment.objects.filter(parent=self).all().count()

	@property 
	def children(self):
		return Comment.objects.filter(parent=self).order_by('-created').all()

	@property
	def is_parent(self):
		if self.parent is None:
			return True
		return False

class CommentLike(models.Model):
	user = models.ForeignKey(Profile, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
	value = models.CharField(choices=LIKE_CHOICES, max_length=8)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)
	ip_address = models.CharField(max_length=25, default='00.000.000.000', blank=True, null=True)

	def __str__(self):
		return f" | CommentLike({self.user}-{self.comment}-{self.value})"

class Notification(models.Model):
	# 1 = Like, 2 = Comment, 3 = Follow, 4 = Message
	notification_type = models.IntegerField()
	to_user = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE, null=True)
	from_user = models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE, null=True)
	post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
	comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
	thread = models.ForeignKey('ThreadModel', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
	date = models.DateTimeField(default=timezone.now)
	user_has_seen = models.BooleanField(default=False)

class ThreadModel(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
	receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')

	def __str__(self):
		return f"Message thread between user:{self.user} and receiver:{self.receiver}"

class MessageModel(models.Model):
	thread = models.ForeignKey('ThreadModel', related_name='+', on_delete=models.CASCADE, blank=True, null=True)
	sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
	receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
	body = models.CharField(max_length=1000)
	image = models.ImageField(upload_to='message_photos', blank=True, null=True)
	date = models.DateTimeField(default=timezone.now)
	is_read = models.BooleanField(default=False) 

