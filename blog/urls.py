from django.urls import path 
from . views import (
	PostListView, 
	PostDetailView, 
	PostCreateView, 
	PostUpdateView,
	PostDeleteView,
	UserPostListView,
	SearchResultsView,
	UserResultsView,
	CategoryResultsView,
	like_unlike_post
)
from . import views

urlpatterns = [
	path('', PostListView.as_view(), name='blog-home'),
	path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
	path('search/', UserResultsView.as_view(), name='user_results'),
	path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
	path('post/new/', PostCreateView.as_view(), name='post-create'),
	path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
	path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
	path('post/search/', SearchResultsView.as_view(), name='search-results'),
	path('category/<str:category>/', CategoryResultsView.as_view(), name='cat-results'),
	#path('profile/<int:pk>/', ProfileListView.as_view(template_name='blog/profile_list.html'), name='profile-view'),
	path('post/liked/', views.like_unlike_post, name='like-post-view'),
	path('post/comment/', views.comment_post, name='comment-post-view'),
	path('about/', views.about, name='blog-about')
]