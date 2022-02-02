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
from . models import Post, PostImage, Like, Category
from users.models import Profile
from django.db.models import Q
from itertools import chain
from . forms import ImageForm, ImageFormSet, CommentModelForm
from django.db import transaction
from django.http import JsonResponse
from django.forms.models import model_to_dict


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

class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html'
	context_object_name = 'posts'
	paginate_by = 5

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')

	def get_context_data(self, *args, **kwargs):
		context = super(UserPostListView, self).get_context_data(*args, **kwargs)
		context['cats_menu'] = Category.objects.all()
		context['user_pro'] = User.objects.filter(username=get_object_or_404(User, username=self.kwargs.get('username'))).first()
		return context

	# def get_context_data(self, **kwargs):
	# 	context = super(UserPostListView, self).get_context_data(**kwargs)
	# 	context['user_pro'] = User.objects.filter(username=get_object_or_404(User, username=self.kwargs.get('username'))).first()
	# 	return context

class PostDetailView(DetailView):
	model = Post 

	def get_context_data(self, *args, **kwargs):
		cats_menu = Category.objects.all()
		context = super(PostDetailView, self).get_context_data(*args, **kwargs)
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
	user = request.user #can delete?
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
			'likes': post_obj.liked.all().count()
		}
		return JsonResponse(data, safe=False)
	return redirect('blog-home')


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
			# data = {
			# 	'comment': instance
			# }
			#c_form = CommentModelForm()
			context = {
				'comment': model_to_dict(instance),
				'username': profile.user.username,
				'image': profile.image.url
			}
			return JsonResponse(context, status=200)
			# return JsonResponse({'comment': model_to_dict(instance)}, instance.username, status=200)
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
