from django.urls import path 
from . views import (
	PostListView, 
	PostDetailView, 
	LatestCommentsPostDetailView,
	PostCreateView, 
	PostUpdateView,
	PostDeleteView,
	UserPostListView,
	UserPostByCatListView,
	SearchResultsView,
	UserResultsView,
	CategoryResultsView,
	like_unlike_post,
	del_comment,
	del_parent_comment,
	del_com_temp,
	load_more_comments_detail,
	load_more_comments_detail_bylatest,
	CommentReplyView,
	post_comment_detail_view,
	load_more_replies_detail_bylatest,
	PostNotification,
	CommentReplyNotification,
	FollowNotification,
	RemoveNotification,
	ThreadNotification,
	ListThread,
	CreateThread,
	ThreadView,
	CreateMessage,
	profile_to_thread,	
)
from . import views

urlpatterns = [
	path('', PostListView.as_view(), name='blog-home'),
	path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
	path('user/<str:username>/category/<str:category>/', UserPostByCatListView.as_view(), name='user-posts-bycat'),
	path('search/', UserResultsView.as_view(), name='user_results'),
	path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
	path('post/load-more-comments-detail/', views.load_more_comments_detail, name='load-more-comments-detail'),
	path('post/load-more-comments-detail-bylatest/', views.load_more_comments_detail_bylatest, name='load-more-comments-detail-bylatest'),
	path('post/<int:pk>/latest/', LatestCommentsPostDetailView.as_view(), name='latest-comment-post-detail'),
	path('post/new/', PostCreateView.as_view(), name='post-create'),
	path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
	path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
	path('post/search/', SearchResultsView.as_view(), name='search-results'),
	path('category/<str:category>/', CategoryResultsView.as_view(), name='cat-results'),
	#path('profile/<int:pk>/', ProfileListView.as_view(template_name='blog/profile_list.html'), name='profile-view'),
	path('post/liked/', views.like_unlike_post, name='like-post-view'),
	path('post/comment/', views.comment_post, name='comment-post-view'),
	path('post/<int:post_pk>/comment/<int:comment_pk>/reply', CommentReplyView.as_view(), name='comment-reply'),
	#path('post/<int:post_pk>/comment/<int:comment_pk>', PostCommentDetailView.as_view(), name='post-comment-detail-v'),
	path('post/<int:post_pk>/comment/<int:comment_pk>', views.post_comment_detail_view, name='post-comment-detail'),
	path('post/load-more-replies-detail-bylatest/', views.load_more_replies_detail_bylatest, name='load-more-replies-detail-bylatest'),
	path('post/comment/like/', views.like_unlike_comment, name='like-comment-view'),
	path('post/comment/<int:pk>/delete/', views.del_comment, name='comment-delete'),
	path('post/parent-comment/<int:pk>/delete/', views.del_parent_comment, name='parent-comment-delete'),
	path('post/commenttemp/<int:pk>/delete/', views.del_com_temp, name='comment-delete-temp'),
	path('notification/<int:notification_pk>/post/<int:post_pk>/', PostNotification.as_view(), name='post-notification'),
	path('notification/<int:notification_pk>/post/<int:post_pk>/<int:comment_pk>/', CommentReplyNotification.as_view(), name='comment-reply-notification'),
	path('notification/<int:notification_pk>/profile/<int:profile_pk>/', FollowNotification.as_view(), name='follow-notification'),
	path('notification/<int:notification_pk>/thread/<int:thread_pk>/', ThreadNotification.as_view(), name='thread-notification'),
	path('notification/delete/<int:notification_pk>/', RemoveNotification.as_view(), name='notification-delete'),
	path('inbox/', ListThread.as_view(), name='inbox'),
	path('inbox/create-thread/', CreateThread.as_view(), name='create-thread'),
	path('inbox/<int:pk>/', ThreadView.as_view(), name='thread'),
	path('inbox/<int:pk>/create-message/', CreateMessage.as_view(), name='create-message'),
	path('inbox/<int:profile_pk>/profile-message/', views.profile_to_thread, name='profile-message'),
	path('about/', views.about, name='blog-about'),
]