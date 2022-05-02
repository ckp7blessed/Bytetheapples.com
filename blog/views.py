from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from django.views.generic import (
	ListView, 
	DetailView, 
	CreateView, 
	UpdateView, 
	DeleteView
) 
from . models import Post, PostImage, Like, Category, Comment, CommentLike
from users.models import Profile
from django.db.models import Q, Count, OuterRef, Prefetch
from itertools import chain
from . forms import ImageForm, ImageFormSet, CommentModelForm
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.core import serializers
from . templatetags import custom_tags
from django.template.defaultfilters import timesince, date


# Create your views here.

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

	#original
	# def get_queryset(self):
	# 	user = get_object_or_404(User, username=self.kwargs.get('username'))
	# 	return Post.objects.filter(author=user).order_by('-date_posted')

	#{% for comment in post.comment_set.all %}

	# def get_context_data(self, *args, **kwargs):
	# 	# context = super(UserPostListView, self).get_context_data(*args, **kwargs)
	# 	context = super().get_context_data(*args, **kwargs)
	# 	user = get_object_or_404(User, username=self.kwargs.get('username'))
	# 	context['cats_menu'] = Category.objects.all()
	# 	context['user_pro'] = User.objects.filter(username=user).first()
	# 	return context

	def get_context_data(self, *args, **kwargs):
		# context = super(UserPostListView, self).get_context_data(*args, **kwargs)
		context = super().get_context_data(*args, **kwargs)
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		context['cats_menu'] = Category.objects.all()
		context['user_pro'] = User.objects.filter(username=get_object_or_404(User, username=self.kwargs.get('username'))).first()
		return context 

		#context['posts'] = Post.objects.filter(author=user).order_by('-date_posted')

		# posts = Post.objects.filter(author=user).order_by('-date_posted').all()
		# for post in posts:
		# 	context['comment_list'] = post.comment_set.all().order_by("-liked")
		# 	#context['comment_list'] = post.prefetch_related(
		# 		# 	Prefetch(
		# 		# 		"comment_set",
		# 		# 		# Specify the queryset to annotate and order by Count("liked")
		# 		# 		#queryset = Post.objects.annotate(like_count=Count('liked')).order_by('-like_count')
		# 		# 		queryset=Comment.objects.annotate(
		# 		# 			like_count=Count("liked")
		# 		# 		).order_by("-like_count"),
		# 		# 		# Prefetch into post.comment_list
		# 		# 		to_attr="comment_list",
		# 		# 	)
		# 		# )
		# 	return context




		# doesnt really work, nothing happens
		# context['post'] = Post.objects.prefetch_related(
		# 		Prefetch(
		# 			"comment_set",
		# 			# Specify the queryset to annotate and order by Count("liked")
		# 			#queryset = Post.objects.annotate(like_count=Count('liked')).order_by('-like_count')
		# 			queryset=Comment.objects.annotate(
		# 				like_count=Count("liked")
		# 			).order_by("-like_count"),
		# 			# Prefetch into post.comment_list
		# 			to_attr="comment_list",
		# 		)
		# 	)
		# print(context)
		# return context


class PostDetailView(DetailView):
	model = Post 

	def get_context_data(self, *args, **kwargs):
		cats_menu = Category.objects.all()
		context = super(PostDetailView, self).get_context_data(*args, **kwargs)
		context['cats_menu'] = cats_menu
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

# def load_more_comments_detail(request):
# 	offset = int(request.POST['offset'])
# 	print(f'offset{offset}')
# 	limit = offset
# 	post_id = request.POST.get('post_id')
# 	post = Post.objects.filter(id=post_id).first()
# 	comments = Comment.objects.filter(post=post).all().order_by('-liked')
# 	print(f'comments list - {comments}')
# 	comment = comments[limit]
# 	print(f'comment offset= {comment}')

# 	u_name = comment.user
# 	u_image = comment.user.image.url
# 	c_create = comment.created
# 	dated = date(c_create, "F d, Y")
# 	print(dated)
# 	t_since = timesince(c_create)
# 	print(f't_since{t_since}')

# 	up_to = custom_tags.upto(t_since)
# 	print(f'up_to{up_to}')

# 	if up_to == "show_date":
# 		created = dated
# 	elif up_to == "Just Now":
# 		created = up_to
# 	else:
# 		created = f'{up_to} ago'
# 	print(f'created == {created}')

# 	print(f'username = {u_name}')
# 	print(offset, limit+offset, limit)

# 	total_comments = comments.all().count()
# 	print(f'total_comments{total_comments}')
# 	#print(f'username ={comments.user}')
# 	comments_json = serializers.serialize('json', comment)
# 	data = {
# 		'comment': comments_json,
# 		#'comments': model_to_dict(comments),
# 		'username': str(u_name),
# 		'image': u_image,
# 		'user_url_start': "user/",
# 		'comment_like_url': "post/comment/like/",
# 		'created': created,
# 		'total_comments': total_comments
# 	}
# 	return JsonResponse(data, safe=False)

def load_more_comments_detail(request):
	offset = int(request.POST['offset'])
	print('\n'*3)
	print(f'offset{offset}')
	limit = 5
	post_id = request.POST.get('post_id')
	post = Post.objects.filter(id=post_id).first()
	#comments = Comment.objects.filter(post=post).all().order_by('-liked')
	
	comments_to_sort = Comment.objects.filter(post=post).all()
	comments = sorted(comments_to_sort, key=lambda comment: comment.num_likes(), reverse=True )

	total = Comment.objects.filter(post=post).all().count()
	print(f'comments list - {comments}')
	print(f'----------{total} COMMENTS ---------')
	print(f'offset range=[{offset}:{offset+limit}]')

	# if offset+limit > total:
	# 	comments = comments[offset+1:offset+limit]

	comments = comments[offset:offset+limit]
	#counts = comments.count()
	print('\n')
	print(f'comments offset= {comments}')
	#print(f'comments offset COUNT = {comments}')

	profile = Profile.objects.get(user=request.user)

	for comment in comments:
		print("------------------")
		print(comment)
		print(comment.body)
		u_name = comment.user
		u_image = comment.user.image.url

		like_count = comment.num_likes()
		print(f'LIKE COUNT ====={like_count}')

		c_create = comment.created
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
		print(f'created == {created}')
		print(f'username = {u_name}')

		liked_list = []
		liked_list_images = []
		for liked_user in comment.liked.all():
			liked_user_username = liked_user.user.username
			print(liked_user_username)
			liked_list.append(liked_user_username)
			liked_user_image = liked_user.image.url
			print(liked_user_image)
			liked_list_images.append(liked_user_image)
		print(liked_list)
		print('\n')
		print(liked_list_images)
		# if profile in comment.liked.all():
		# 	like_value = "Unlike"
		# 	print('true')
		# 	print(profile.user)
		# else:
		# 	like_value = "Like"
		# 	print('false')

	print(offset, limit+offset)
	
	#total_comments = comments.all().count()
	#print(f'total_comments{total_comments}')



	comments_json = serializers.serialize('json', comments)
	data = {
		'comment': comments_json,
		#'comments': model_to_dict(comments),
		'username': str(u_name),
		'image': u_image,
		#'user_url_start': "user/",
		#'comment_like_url': "post/comment/like/",
		'created': created,
		#'likevalue': like_value,
		'like_count': like_count,
		'user': profile.id,
		'liked_list': liked_list,
		'liked_list_images': liked_list_images
		#'total_comments': total_comments,
		#'nomore': nomore
	}
	return JsonResponse(data, safe=False)


				# 'comment': model_to_dict(instance),
				# 'username': profile.user.username,
				# 'image': profile.image.url,
				# 'user_url_start': "user/",
				# 'comment_like_url': "post/comment/like/",
				# 'delete_url_start': "post/commenttemp/",
				# 'delete_url_end': "/delete/",


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
					queryset=Comment.objects.order_by("-created"),
					# Prefetch into post.comment_list
					to_attr="comment_list",
				)
			)
		)

	def get_context_data(self, *args, **kwargs):
		cats_menu = Category.objects.all()
		context = super().get_context_data(*args, **kwargs)
		context['cats_menu'] = cats_menu
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
		object_list = Post.objects.filter(Q(content__icontains=query) | Q(title__icontains=query)).order_by('-date_posted')
		return object_list

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
	c_form = CommentModelForm()

	if request.method == "POST":
		c_form = CommentModelForm(request.POST)
		if c_form.is_valid():
			instance = c_form.save(commit=False)
			instance.user = profile
			instance.username = profile.user.username
			instance.post = Post.objects.get(id=request.POST.get('post_id'))
			instance.save()
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


# WITH AJAX - TEST
# def comment_post(request):
# 	profile = Profile.objects.get(user=request.user)
# 	c_form = CommentModelForm()

# 	if request.method == "POST":
# 		c_form = CommentModelForm(request.POST)
# 		if c_form.is_valid():
# 			instance = c_form.save(commit=False)
# 			instance.user = profile
# 			instance.post = Post.objects.get(id=request.POST.get('post_id'))
# 			instance.save()
# 			c_form = CommentModelForm()
# 			return JsonResponse({'comment': model_to_dict(instance)}, status=200, safe=False)
# 	return redirect('blog-home')



#ORIGINAL WITHOUT AJAX - CLEANED UP
# def comment_post(request):
# 	profile = Profile.objects.get(user=request.user)
# 	c_form = CommentModelForm()

# 	if 'submit_c_form' in request.POST:
# 		c_form = CommentModelForm(request.POST)
# 		if c_form.is_valid():
# 			instance = c_form.save(commit=False)
# 			instance.user = profile
# 			instance.post = Post.objects.get(id=request.POST.get('post_id'))
# 			instance.save()
# 			c_form = CommentModelForm()
# 		return redirect('blog-home')



#ORIGINAL WITHOUT AJAX
# def comment_post(request):
# 	profile = Profile.objects.get(user=request.user)
# 	c_form = CommentModelForm()
# 	# c_form = CommentModelForm(request.POST or None)

# 	if 'submit_c_form' in request.POST:
# 		c_form = CommentModelForm(request.POST)
# 		if c_form.is_valid():
# 			instance = c_form.save(commit=False)
# 			instance.user = profile
# 			instance.post = Post.objects.get(id=request.POST.get('post_id'))
# 			instance.save()
# 			c_form = CommentModelForm()
# 			#context = {'c_form': c_form}
# 			#return render(request, context)
# 			#return render(request, 'blog/home.html')
# 		#return redirect('post-detail', instance.post.pk)

def about(request):
	return render(request, 'blog/about.html', {'title':'About'})
