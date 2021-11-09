from django.shortcuts import render, redirect
from . forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.views.generic.edit import DeleteView
from blog.models import Post
from django.urls import reverse_lazy

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

	def get_queryset(self):
		#ser = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=self.request.user).order_by('-date_posted')

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

