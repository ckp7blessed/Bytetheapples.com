from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from django.views.generic import (
	View,
	ListView, 
	DetailView, 
	CreateView,  
	UpdateView, 
	DeleteView
) 
from . models import Post, PostImage, Like, Category, Comment, CommentLike, Notification
from users.models import Profile
from django.db.models import Q, Count, OuterRef, Prefetch
from itertools import chain
from . forms import ImageForm, ImageFormSet, CommentModelForm
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.core import serializers
from . templatetags import custom_tags
from django.template.defaultfilters import timesince, date
from django.utils.dateparse import parse_datetime
import json


def home(request):
	context = {
		'posts': Post.objects.all()
	}
	return render(request, 'blog/home.html', context)

class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5

	def get_context_data(self, *args, **kwargs):
		cats_menu = Category.objects.all()
		c_form = CommentModelForm(self.request.POST or None)
		context = super(PostListView, self).get_context_data(*args, **kwargs)
		context['cats_menu'] = cats_menu
		context['c_form'] = c_form
		return context

	def get_queryset(self):
		return (
			super()
			.get_queryset()
			# Prefetch comment using a Prefetch object gives you more control
			.prefetch_related(
				Prefetch(
					"comment_set",
					# Specify the queryset to annotate and order by Count("liked")
					#queryset = Post.objects.annotate(like_count=Count('liked')).order_by('-like_count')
					queryset=Comment.objects.annotate(
						like_count=Count("liked")
					).order_by("-like_count"),
					# Prefetch into post.comment_list
					to_attr="comment_list",
				)
			)
		)

class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html'
	context_object_name = 'posts'
	paginate_by = 5

	def get_queryset(self):
		return (
			super()
			.get_queryset()
			# Filter by author/user
			.filter(author__username=self.kwargs.get('username')).order_by('-date_posted')
			# Prefetch comment using a Prefetch object gives you more control
			.prefetch_related(
				Prefetch(
					"comment_set",
					# Specify the queryset to annotate and order by Count("liked")
					queryset=Comment.objects.annotate(
						like_count=Count("liked")
					).order_by("-like_count"),
					# Prefetch into post.comment_list
					to_attr="comment_list",
				)
			)
		)

	def get_context_data(self, *args, **kwargs):
		# context = super(UserPostListView, self).get_context_data(*args, **kwargs)
		context = super().get_context_data(*args, **kwargs)
		c_form = CommentModelForm(self.request.POST or None)
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		profile = Profile.objects.get(user=user)
		followers = profile.followers.all()
		following = Profile.objects.filter(followers__in=[user])
		if followers:
			for follower in followers:
				if follower == self.request.user:
					is_following = True
					break
				else:
					is_following = False
		else:
			is_following = False
		number_of_followers = followers.count()

		users_categories = user.post_set.all().values_list("category__category_name", flat=True).exclude(category=None).distinct().order_by("category__category_name")
		context['users_categories'] = users_categories
		context['user_pro'] = User.objects.filter(username=get_object_or_404(User, username=self.kwargs.get('username'))).first()
		context['following'] = following
		context['followers'] = followers 
		context['is_following'] = is_following
		context['number_of_followers'] = number_of_followers
		context['cats_menu'] = Category.objects.all()
		context['c_form'] = c_form
		return context 

class UserPostByCatListView(ListView):
	model = Post
	template_name = 'blog/user_posts_bycategory.html'
	context_object_name = 'posts'
	paginate_by = 5

	def get_queryset(self):
		cat = get_object_or_404(Category, category_name=self.kwargs.get('category'))
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		# return user.post_set.all().filter(category=cat).all().order_by('-date_posted')
		return (
			super()
			.get_queryset()
			# Filter by author/user
			.filter(author__username=self.kwargs.get('username')).filter(category=cat).order_by('-date_posted')
			# Prefetch comment using a Prefetch object gives you more control
			.prefetch_related(
				Prefetch(
					"comment_set",
					# Specify the queryset to annotate and order by Count("liked")
					queryset=Comment.objects.annotate(
						like_count=Count("liked")
					).order_by("-like_count"),
					# Prefetch into post.comment_list
					to_attr="comment_list",
				)
			)
		)

	def get_context_data(self, *args, **kwargs):
		# context = super(UserPostListView, self).get_context_data(*args, **kwargs)
		context = super().get_context_data(*args, **kwargs)
		c_form = CommentModelForm(self.request.POST or None)
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		profile = Profile.objects.get(user=user)
		followers = profile.followers.all()
		following = Profile.objects.filter(followers__in=[user])
		if followers:
			for follower in followers:
				if follower == self.request.user:
					is_following = True
					break
				else:
					is_following = False
		else:
			is_following = False
		number_of_followers = followers.count()
		users_categories = user.post_set.all().values_list("category__category_name", flat=True).exclude(category=None).distinct().order_by("category__category_name")
		context['users_categories'] = users_categories
		context['cats_menu'] = Category.objects.all()
		context['user_pro'] = User.objects.filter(username=get_object_or_404(User, username=self.kwargs.get('username'))).first()
		context['following'] = following
		context['followers'] = followers 
		context['is_following'] = is_following
		context['number_of_followers'] = number_of_followers
		context['c_form'] = c_form
		return context 

class PostDetailView(DetailView):
	model = Post 

	def get_context_data(self, *args, **kwargs):
		cats_menu = Category.objects.all()
		c_form = CommentModelForm(self.request.POST or None)
		context = super(PostDetailView, self).get_context_data(*args, **kwargs)
		context['cats_menu'] = cats_menu
		context['c_form'] = c_form
		return context

	def get_queryset(self):
		return (
			super()
			.get_queryset()
			# Prefetch comment using a Prefetch object gives you more control
			.prefetch_related(
				Prefetch(
					"comment_set",
					# Specify the queryset to annotate and order by Count("liked")
					#queryset = Post.objects.annotate(like_count=Count('liked')).order_by('-like_count')
					queryset=Comment.objects.filter(parent=None).annotate(
						like_count=Count("liked")
					).order_by("-like_count"),
					# Prefetch into post.comment_list
					to_attr="comment_list",
				)
			)
		)

def post_comment_detail_view(request, post_pk, comment_pk, *args, **kwargs):
	post = get_object_or_404(Post, pk=post_pk)
	comment = get_object_or_404(Comment, pk=comment_pk)
	c_form = CommentModelForm(request.POST or None)
	cats_menu = Category.objects.all()

	context = {
		'post': post,
		'comment': comment,
		'c_form': c_form,
		'cats_menu': cats_menu
	}
	return render(request, 'blog/post_comment_detail.html', context)


class CommentReplyView(LoginRequiredMixin, View):
	def post(self, request, post_pk, comment_pk, *args, **kwargs):
		post = Post.objects.get(pk=post_pk)
		parent_comment = Comment.objects.get(pk=comment_pk)
		profile = Profile.objects.get(user=request.user)
		c_form = CommentModelForm(request.POST)

		if c_form.is_valid():
			instance = c_form.save(commit=False)
			instance.user = profile
			instance.username = profile.user.username
			instance.post = post
			instance.parent = parent_comment
			instance.save()
			notification = Notification.objects.create(notification_type=2, from_user=request.user, 
				to_user=parent_comment.user.user, comment=parent_comment)
			print(notification)
			print(instance, instance.user, instance.body, instance.username)
		return redirect('post-comment-detail', post_pk=post_pk, comment_pk=comment_pk)	
		#return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


#INFINITE SCROLL LOADING REPLIES BY LATEST
def load_more_replies_detail_bylatest(request):
	offset = int(request.POST['offset'])
	print(offset)
	# offset = {% for comment in post.comment_list|slice:"0:7" %} - comments.html
	limit = 5 # sending 5 comments at a time
	post_id = request.POST.get('post_id')
	post = Post.objects.get(id=post_id)

	comment_parent_id = request.POST.get('comment_parent_id')
	comment_parent = Comment.objects.get(pk=comment_parent_id)
	comments = comment_parent.children
	comments = comments[offset:offset+limit]
	
	# comments = Comment.objects.filter(post=post).all().filter(parent=None).order_by('-created')
	# comments = comments[offset:offset+limit]
	print(comments)

	if request.user.is_anonymous:
		profile_id = None
	else:
		profile = Profile.objects.get(user=request.user)
		profile_id = profile.id

	comments_json = serializers.serialize('json', comments)
	print('--------comment_json (serialized)-------')
	print(comments_json)
	print('/n')
	comments_dict = json.loads(comments_json)
	print('--------comments_dict (json.loads)-------')
	print(comments_dict)
	print('/n')

	for comment in comments_dict:
		liked_users_profile_list = []
		liked_users_profile_pic_list = []

		userid = comment['fields']['user']
		user_profile = Profile.objects.get(id=userid)
		comment['fields']['username'] = user_profile.user.username
		comment['fields']['user_pp'] = user_profile.image.url

		c_create = parse_datetime(comment['fields']['created'])
		dated = date(c_create, "F d, Y")
		t_since = timesince(c_create)
		up_to = custom_tags.upto(t_since)
		if up_to == "show_date":
			created = dated
		elif up_to == "Just Now":
			created = up_to
		else:
			created = f'{up_to} ago'
		comment['fields']['created_custom'] = created

		# comment_id = Comment.objects.get(pk=comment['pk'])
		# comment['fields']['reply_count'] = comment_id.children.count()

		for liked_users_id in comment['fields']['liked']:

			liked_users_profile = Profile.objects.get(id=liked_users_id)
			liked_users_profile_list.append(liked_users_profile.user.username)
			liked_users_profile_pic_list.append(liked_users_profile.image.url)
			comment['fields']['liked_username'] = liked_users_profile_list
			comment['fields']['liked_user_pp'] = liked_users_profile_pic_list


	comments_json = json.dumps(comments_dict)
	print('--------comments_json (json.dumps)-------')
	print(comments_json)
	print('/n')

	data = {
		'comment': comments_json,
		'user': profile_id,
	}
	print('--------------------------!!!!!!!!-------')
	print(data)
	return JsonResponse(data, safe=False)


# @login_required
# def comment_post(request):
# 	profile = Profile.objects.get(user=request.user)
# 	c_form = CommentModelForm()

# 	if request.method == "POST":
# 		c_form = CommentModelForm(request.POST)
# 		if c_form.is_valid():
# 			instance = c_form.save(commit=False)
# 			instance.user = profile
# 			instance.username = profile.user.username
# 			instance.post = Post.objects.get(id=request.POST.get('post_id'))
# 			instance.save()
# 			print(instance, instance.user, instance.body, instance.username)

# 			data = {
# 				'comment': model_to_dict(instance),
# 				'username': profile.user.username,
# 				'image': profile.image.url,
# 				'user_url_start': "/user/",
# 				'comment_like_url': "post/comment/like/",
# 				'delete_url_start': "post/commenttemp/",
# 				'delete_url_end': "/delete/",

# 			}
# 			return JsonResponse(data, status=200)
# 			# return JsonResponse({'comment': model_to_dict(instance)}, instance.username, status=200)
# 		return redirect('blog-home')



#INFINITE SCROLL LOADING COMMENTS 
def load_more_comments_detail(request):
	offset = int(request.POST['offset'])
	# offset = {% for comment in post.comment_list|slice:"0:7" %} - comments.html
	print('\n'*3)
	print(f'offset{offset}')
	limit = 5 # sending 5 comments via ajax
	post_id = request.POST.get('post_id')
	post = Post.objects.get(id=post_id)
	
	comments_to_sort = Comment.objects.filter(post=post).all().filter(parent=None)
	comments = sorted(comments_to_sort, key=lambda comment: comment.num_likes(), reverse=True )

	# total = Comment.objects.filter(post=post).all().count()
	# for comment in comments:
	# 	print(f'comments list - {comment.id}ID and {comment.body} by {comment.user}')
	# print(f'----------{total} COMMENTS ---------')
	# print(f'offset range=[{offset}:{offset+limit}]')
	comments = comments[offset:offset+limit]

	print('--------------------------')
	print('\n'*2)
	print(f'OFFSET COMMENTS --- {comments}')

	if request.user.is_anonymous:
		profile_id = None
	else:
		profile = Profile.objects.get(user=request.user)
		profile_id = profile.id
	
	comments_json = serializers.serialize('json', comments)
	print('------------------------serialize--------------')
	print(f'comments before serialized.......{comments}')
	print('\n'*2)
	print(f'comments_json serialized......{comments_json}')

	comments_dict = json.loads(comments_json)
	print('------------------------comments dict--------------')
	print(comments_dict)

	for comment in comments_dict:

		liked_users_profile_list = []
		liked_users_profile_pic_list = []

		userid = comment['fields']['user']
		user_profile = Profile.objects.get(id=userid)
		print('\n'*2)
		print('userid')
		print(user_profile.user.username)
		comment['fields']['username'] = user_profile.user.username
		print(user_profile.image.url)
		comment['fields']['user_pp'] = user_profile.image.url

		c_create = parse_datetime(comment['fields']['created'])
		dated = date(c_create, "F d, Y")
		print(dated)
		t_since = timesince(c_create)
		print(f't_since{t_since}')

		up_to = custom_tags.upto(t_since)
		print(f'up_to{up_to}')

		if up_to == "show_date":
			created = dated
		elif up_to == "Just Now":
			created = up_to
		else:
			created = f'{up_to} ago'

		comment['fields']['created_custom'] = created

		comment_id = Comment.objects.get(pk=comment['pk'])
		comment['fields']['reply_count'] = comment_id.children.count()

		for liked_users_id in comment['fields']['liked']:
			liked_users_profile = Profile.objects.get(id=liked_users_id)
			liked_users_profile_list.append(liked_users_profile.user.username)
			liked_users_profile_pic_list.append(liked_users_profile.image.url)
			comment['fields']['liked_username'] = liked_users_profile_list
			comment['fields']['liked_user_pp'] = liked_users_profile_pic_list

	comments_json = json.dumps(comments_dict)
	print(comments_json)

	data = {
		'comment': comments_json,
		'user': profile_id,
		#'nomore': nomore
	}
	print('--------------------------!!!!!!!!-------')
	print(data)
	return JsonResponse(data, safe=False)


#INFINITE SCROLL LOADING COMMENTS BY LATEST
def load_more_comments_detail_bylatest(request):
	offset = int(request.POST['offset'])
	print(offset)
	# offset = {% for comment in post.comment_list|slice:"0:7" %} - comments.html
	limit = 5 # sending 5 comments at a time
	post_id = request.POST.get('post_id')
	post = Post.objects.get(id=post_id)
	
	comments = Comment.objects.filter(post=post).all().filter(parent=None).order_by('-created')
	comments = comments[offset:offset+limit]
	print(comments)

	if request.user.is_anonymous:
		profile_id = None
	else:
		profile = Profile.objects.get(user=request.user)
		profile_id = profile.id

	comments_json = serializers.serialize('json', comments)
	comments_dict = json.loads(comments_json)

	for comment in comments_dict:
		liked_users_profile_list = []
		liked_users_profile_pic_list = []

		userid = comment['fields']['user']
		user_profile = Profile.objects.get(id=userid)
		comment['fields']['username'] = user_profile.user.username
		comment['fields']['user_pp'] = user_profile.image.url

		c_create = parse_datetime(comment['fields']['created'])
		dated = date(c_create, "F d, Y")
		t_since = timesince(c_create)
		up_to = custom_tags.upto(t_since)
		if up_to == "show_date":
			created = dated
		elif up_to == "Just Now":
			created = up_to
		else:
			created = f'{up_to} ago'
		comment['fields']['created_custom'] = created

		comment_id = Comment.objects.get(pk=comment['pk'])
		comment['fields']['reply_count'] = comment_id.children.count()

		for liked_users_id in comment['fields']['liked']:

			liked_users_profile = Profile.objects.get(id=liked_users_id)
			liked_users_profile_list.append(liked_users_profile.user.username)
			liked_users_profile_pic_list.append(liked_users_profile.image.url)
			comment['fields']['liked_username'] = liked_users_profile_list
			comment['fields']['liked_user_pp'] = liked_users_profile_pic_list


	comments_json = json.dumps(comments_dict)

	data = {
		'comment': comments_json,
		'user': profile_id,
	}
	return JsonResponse(data, safe=False)

class LatestCommentsPostDetailView(DetailView):
	model = Post 
	template_name = 'blog/latest_comments_post_detail.html'

	def get_queryset(self):
		return (
			super()
			.get_queryset()
			# Prefetch comment using a Prefetch object gives you more control
			.prefetch_related(
				Prefetch(
					"comment_set",
					# Specify the queryset to annotate and order by Count("liked")
					#queryset = Post.objects.annotate(like_count=Count('liked')).order_by('-like_count')
					queryset=Comment.objects.filter(parent=None).order_by("-created"),
					# Prefetch into post.comment_list
					to_attr="comment_list",
				)
			)
		)

	def get_context_data(self, *args, **kwargs):
		cats_menu = Category.objects.all()
		context = super().get_context_data(*args, **kwargs)
		c_form = CommentModelForm(self.request.POST or None)
		context['cats_menu'] = cats_menu
		context['c_form'] = c_form
		return context

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post 
	fields = ['title', 'content', 'category']

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['image_formset'] = ImageFormSet()
		return context

	def form_valid(self, form):
		form.instance.author = self.request.user
		image_formset = ImageFormSet(self.request.POST, self.request.FILES) 
		with transaction.atomic():
			self.object = form.save()

			if image_formset.is_valid():
				image_formset.instance = self.object 
				postform = ImageFormSet(self.request.POST) #can delete?
				imageform = ImageFormSet(self.request.FILES)
				for img in self.request.FILES.getlist('postimage_set-0-image'):
					photo = PostImage.objects.create(post=self.object, image=img)
					photo.save()
				messages.success(self.request, 'Your post has been created!')
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post 
	fields = ['title', 'content', 'category']

	def form_valid(self, form):
		form.instance.author = self.request.user 
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post 
	success_url = reverse_lazy('profile')

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

	def delete(self, request, *args, **kwargs):
		response = super().delete(request, *args, **kwargs)
		messages.success(self.request, 'Your post has been deleted!')
		return response

class SearchResultsView(ListView):
	model = Post 
	template_name = 'blog/search_results.html'
	paginate_by = 5

	def get_queryset(self):
		query = self.request.GET.get("q")
		posts = Post.objects.filter(Q(content__icontains=query) | Q(title__icontains=query)).order_by('-date_posted')
		return posts

	# def get_queryset(self):
	# 	query = self.request.GET.get("q")
	# 	object_list = Post.objects.filter(Q(content__icontains=query) | Q(title__icontains=query)).order_by('-date_posted')
	# 	return object_list

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['query'] = self.request.GET.get('q')
		return context

class UserResultsView(ListView):
	model = User 
	template_name = 'blog/user_results.html'

	def get_queryset(self):
		query = self.request.GET.get("q1")
		object_list = User.objects.filter(username__icontains=query)
		return object_list

class CategoryResultsView(ListView):
	model = Post
	template_name = 'blog/cat_posts.html'
	context_object_name = 'posts'
	paginate_by = 5

	def get_queryset(self):
		cats = get_object_or_404(Category, category_name=self.kwargs.get('category'))
		return Post.objects.filter(category=cats).order_by('-date_posted')

	def get_context_data(self, *args, **kwargs):
		context = super(CategoryResultsView, self).get_context_data(*args, **kwargs)
		context['cats_menu'] = Category.objects.all()
		return context

@login_required
def like_unlike_post(request):
	user = request.user
	if request.method == 'POST':
		post_id = request.POST.get('post_id')
		post_obj = Post.objects.get(id=post_id)
		profile = Profile.objects.get(user=user)

		if profile in post_obj.liked.all():
			post_obj.liked.remove(profile)
		else:
			post_obj.liked.add(profile)
			Notification.objects.create(notification_type=1, from_user=request.user, to_user=post_obj.author, post=post_obj)

		like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

		if not created:
			if like.value=='Like':
				like.value='Unlike'
			else:
				like.value='Like'
		else:
			like.value='Like'

			post_obj.save()
			like.save()

		data = {
			'value': like.value,
			'likes': post_obj.liked.all().count(),
			'username': profile.user.username,
			'user_id': profile.user.id,
			'image': profile.image.url
		}
		return JsonResponse(data, safe=False, status=200)
	return redirect('blog-home')

@login_required
def comment_post(request):
	profile = Profile.objects.get(user=request.user)
	post = Post.objects.get(id=request.POST.get('post_id'))
	c_form = CommentModelForm()

	if request.method == "POST":
		c_form = CommentModelForm(request.POST)
		if c_form.is_valid():
			instance = c_form.save(commit=False)
			instance.user = profile
			instance.username = profile.user.username
			instance.post = post
			instance.save()
			Notification.objects.create(notification_type=2, from_user=request.user, 
				to_user=post.author, post=post)
			print(instance, instance.user, instance.body, instance.username)

			data = {
				'comment': model_to_dict(instance),
				'username': profile.user.username,
				'image': profile.image.url,
				'user_url_start': "/user/",
				'comment_like_url': "post/comment/like/",
				'delete_url_start': "post/commenttemp/",
				'delete_url_end': "/delete/",

			}
			return JsonResponse(data, status=200)
			# return JsonResponse({'comment': model_to_dict(instance)}, instance.username, status=200)
		return redirect('blog-home')

def del_comment(request, *args, **kwargs):
	if request.method == 'POST':
		id = request.POST.get('comment_id')
		comment_obj = Comment.objects.get(id=id)
		comment_id = comment_obj.id
		post_obj = comment_obj.post
		post_id = post_obj.id
		if request.user.id == comment_obj.user.user.id:
			comment_obj.delete()
			num_comments = post_obj.num_comments()

			data = {
				'success': '1',
				'post_id': post_id,
				'comment_id': comment_id,
				'num_comments': num_comments,
				'delete_url_start': "post/comment/",
				'delete_url_end': "/delete/",
			}
		else:
			return redirect('login')
		return JsonResponse(data, safe=False)
	return redirect('blog-home')

def del_com_temp(request, *args, **kwargs):
	if request.method == 'POST':
		id = request.POST.get('comment_id')
		comment_obj = Comment.objects.get(id=id)
		comment_id = comment_obj.id
		post_obj = comment_obj.post
		post_id = post_obj.id
		if request.user.id == comment_obj.user.user.id:
			comment_obj.delete()
			num_comments = post_obj.num_comments()

			data = {
				'success': '1',
				'post_id': post_id,
				'comment_id': comment_id,
				'num_comments': num_comments
			}
		else:
			return redirect('login')
		return JsonResponse(data, safe=False)
	return redirect('blog-home')

@login_required
def like_unlike_comment(request):
	user = request.user #can delete?
	if request.method == 'POST':
		comment_id = request.POST.get('comment_id')
		comment_obj = Comment.objects.get(id=comment_id)
		profile = Profile.objects.get(user=user)
		post = comment_obj.post

		if profile in comment_obj.liked.all():
			comment_obj.liked.remove(profile)
		else:
			comment_obj.liked.add(profile)
			Notification.objects.create(notification_type=1, from_user=request.user, 
				to_user=comment_obj.user.user, comment=comment_obj)

		like, created = CommentLike.objects.get_or_create(user=profile, comment_id=comment_id, post_id=post.id)

		if not created:
			if like.value=='Like':
				like.value='Unlike'
			else:
				like.value='Like'
		else:
			like.value='Like'

			comment_obj.save()
			like.save()
			post.save()
			print(post)

		data = {
			'value': like.value,
			'likes': comment_obj.liked.all().count(),
			'username': profile.user.username,
			'user_id': profile.user.id,
			'image': profile.image.url
		}
		return JsonResponse(data, safe=False)
	return redirect('blog-home')


class PostNotification(View):
	def get(self, request, notification_pk, post_pk, *args, **kwargs):
		notification = Notification.objects.get(pk=notification_pk)
		post = Post.objects.get(pk=post_pk)

		notification.user_has_seen = True
		notification.save()

		return redirect('post-detail', pk=post_pk)

class CommentReplyNotification(View):
	def get(self, request, notification_pk, post_pk, comment_pk, *args, **kwargs):
		notification = Notification.objects.get(pk=notification_pk)
		post = Post.objects.get(pk=post_pk)
		comment = Comment.objects.get(pk=comment_pk)

		notification.user_has_seen = True
		notification.save()

		return redirect('post-comment-detail', post_pk=post_pk, comment_pk=comment_pk)

class FollowNotification(View):
	def get(self, request, notification_pk, profile_pk, *args, **kwargs):
		notification = Notification.objects.get(pk=notification_pk)
		profile = Profile.objects.get(pk=profile_pk)

		notification.user_has_seen = True
		notification.save()

		return redirect('user-posts', username=profile.user.username)

class RemoveNotification(View):
	def get(self, request, notification_pk, *args, **kwargs):
		notification = Notification.objects.get(pk=notification_pk)	

		notification.user_has_seen = True
		notification.save()

		data = {
			'notification_count': Notification.objects.filter(to_user=request.user).exclude(user_has_seen=True).count()
		}

		return JsonResponse(data, safe=False)

def about(request):
	return render(request, 'blog/about.html', {'title':'About'})
