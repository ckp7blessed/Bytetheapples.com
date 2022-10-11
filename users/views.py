from django.shortcuts import render, redirect
from . forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, View
from django.views.generic.edit import DeleteView
from blog.models import Post, Comment, CommentLike, Category, Notification
from blog.forms import CommentModelForm
from users.models import Profile
from django.db.models import Q, Count, OuterRef, Prefetch
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import RequestContext

def get_ip(request):
	try:
		x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
		if x_forward:
			ip = x_forward.split(",")[0]
		else:
			ip = request.META.get("REMOTE_ADDR")
	except:
		ip = ""
	return ip

def register(request):
	if request.method == "POST":
		form = UserRegisterForm(request.POST)
		email = request.POST['email']
		if User.objects.filter(email=email).exists(): 
			messages.error(request, 'The email provided already has an account associated with it')
		elif form.is_valid():	
			user = form.save(commit=False)
			user.username = user.username.lower()
			user.save()
			# username = form.cleaned_data.get('username')
			messages.success(request, f'Account created for {user.username}! You are now able to login.')
			profile = Profile.objects.get(user__username=user.username)
			profile.register_ip = get_ip(request)
			profile.save()
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html', {'form': form})

# LOGGED IN USER'S PROFILE PAGE
class UserProfileListView(LoginRequiredMixin, ListView):
	model = Post
	template_name = 'users/profile.html'
	context_object_name = 'posts'
	paginate_by = 7

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

#FOR USER_POSTS.HTML (toggling follower button on user's profile page js not necessary)
class ToggleFollower(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
		profile = Profile.objects.get(pk=pk)

		if request.user not in profile.followers.all():
			profile.followers.add(request.user)
			Notification.objects.create(notification_type=3, from_user=request.user, to_user=profile.user)
		else:
			profile.followers.remove(request.user)
		return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

#AJAX RESPONSE FOR FOLLOWERS.HTML, FOLLOWING.HTML
def toggle_follower_js(request, *args, **kwargs):
    if request.method != 'POST':
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    pk = request.POST.get('profile_id')
    profile = Profile.objects.get(pk=pk)

    if request.user not in profile.followers.all():
        profile.followers.add(request.user)
        Notification.objects.create(notification_type=3, from_user=request.user, to_user=profile.user)
        return HttpResponse("Following") # JSON response is unnecessary
    else:
        profile.followers.remove(request.user)
        return HttpResponse("Follow")

def handler400(request, exception):
        data = {}
        return render(request,'users/400.html', data)

def handler404(request, exception):
        data = {}
        return render(request,'users/404.html', data)

def handler500(request, exception):
        data = {}
        return render(request,'users/500.html', data)
