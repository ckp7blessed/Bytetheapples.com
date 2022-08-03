from django.shortcuts import render, redirect
from . forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, View
from django.views.generic.edit import DeleteView
from blog.models import Post, Comment, CommentLike, Category
from blog.forms import CommentModelForm
from users.models import Profile
from django.db.models import Q, Count, OuterRef, Prefetch
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

# Create your views here.

def register(request):
	if request.method == "POST":
		form = UserRegisterForm(request.POST)
		if form.is_valid(): 
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created for {username}! You are now able to login.')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html', {'form': form})

class UserProfileListView(LoginRequiredMixin, ListView):
	model = Post
	template_name = 'users/profile.html'
	context_object_name = 'posts'
	paginate_by = 5

	def get_context_data(self, *args, **kwargs):
		cats_menu = Category.objects.all()
		c_form = CommentModelForm(self.request.POST or None)
		context = super(UserProfileListView, self).get_context_data(*args, **kwargs)
		user = self.request.user
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
		context['following'] = following
		context['followers'] = followers 
		context['is_following'] = is_following
		context['number_of_followers'] = number_of_followers
		context['cats_menu'] = cats_menu
		context['c_form'] = c_form
		return context

	def get_queryset(self):
		return (
			super()
			.get_queryset()
			# Filter by author/user
			.filter(author__username=self.request.user).order_by('-date_posted')
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



@login_required
def profile_settings(request):
	if request.method == "POST":
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()

			messages.success(request, 'Your profile has been updated!')
			return redirect('profile')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
		
	context = {
		'u_form': u_form,
		'p_form': p_form,
	}
	return render(request, 'users/profile_settings.html', context)

class UserDeleteView(LoginRequiredMixin, DeleteView):
	model = User 
	success_url = reverse_lazy('blog-home')
	template_name = 'users/user_confirm_delete.html'

	def delete(self, request, *args, **kwargs):
		response = super().delete(request, *args, **kwargs)
		messages.success(self.request, 'Your account has been deleted!')
		return response


#ORIGINAL
# @login_required
# def profile(request):
# 	if request.method == "POST":
# 		u_form = UserUpdateForm(request.POST, instance=request.user)
# 		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
# 		if u_form.is_valid() and p_form.is_valid():
# 			u_form.save()
# 			p_form.save()

# 			messages.success(request, 'Your profile has been updated!')
# 			return redirect('profile')
# 	else:
# 		u_form = UserUpdateForm(instance=request.user)
# 		p_form = ProfileUpdateForm(instance=request.user.profile)
		
# 	context = {
# 		'u_form': u_form,
# 		'p_form': p_form,
# 	}
# 	return render(request, 'users/profile.html', context)

class FollowersListView(LoginRequiredMixin, ListView):
	model = Profile
	template_name = 'users/followers.html'
	context_object_name = 'profile'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		user = self.request.user
		profile = Profile.objects.get(user=user)
		followers = profile.followers.all()
		following = Profile.objects.filter(followers__in=[user])

		number_of_followers = followers.count()

		context['following'] = following
		context['followers'] = followers 
		context['number_of_followers'] = number_of_followers
		context['cats_menu'] = Category.objects.all()
		return context 

	def get_queryset(self):
		return (
			super()
			.get_queryset()
			.get(user=self.request.user))

class FollowingListView(LoginRequiredMixin, ListView):
	model = Profile
	template_name = 'users/following.html'
	context_object_name = 'profile'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		user = self.request.user
		profile = Profile.objects.get(user=user)
		followers = profile.followers.all()
		following = Profile.objects.filter(followers__in=[user])

		number_of_followers = followers.count()

		context['following'] = following
		context['followers'] = followers 
		context['number_of_followers'] = number_of_followers
		context['cats_menu'] = Category.objects.all()
		return context 

	def get_queryset(self):
		return (
			super()
			.get_queryset()
			.get(user=self.request.user))

#FOR USER_POSTS.HTML
class AddFollower(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
		profile = Profile.objects.get(pk=pk)
		profile.followers.add(request.user)
		
		return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
		#return HttpResponseRedirect(self.request.path_info)
		#return redirect('user-posts', pk=profile.pk)		

#FOR USER_POSTS.HTML
class RemoveFollower(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
		profile = Profile.objects.get(pk=pk)
		profile.followers.remove(request.user)
		
		return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
		#return HttpResponseRedirect(self.request.path_info)
		#return redirect('user-posts', pk=profile.pk)	

#AJAX RESPONSE FOR FOLLOWERS.HTML, FOLLOWING.HTML
def add_follower(request, *args, **kwargs):
	if request.method == 'POST':
		id = request.POST.get('profile_id')
		profile = Profile.objects.get(pk=pk)
		profile.followers.add(request.user)

		data = {
			'success': '1',
		}
		return JsonResponse(data, safe=False)
	return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
