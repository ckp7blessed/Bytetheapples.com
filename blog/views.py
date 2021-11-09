from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User 
from django.views.generic import (
	ListView, 
	DetailView, 
	CreateView, 
	UpdateView, 
	DeleteView
) 
from . models import Post
from django.db.models import Q
from itertools import chain

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

class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html'
	context_object_name = 'posts'
	paginate_by = 5

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')

	def get_context_data(self, **kwargs):
		context = super(UserPostListView, self).get_context_data(**kwargs)
		context['user_pro'] = User.objects.filter(username=get_object_or_404(User, username=self.kwargs.get('username'))).first()
		return context

class PostDetailView(DetailView):
	model = Post 

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post 
	fields = ['title', 'content', 'image']

	def form_valid(self, form):
		form.instance.author = self.request.user 
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post 
	fields = ['title', 'content', 'image']

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

def about(request):
	return render(request, 'blog/about.html', {'title':'About'})
