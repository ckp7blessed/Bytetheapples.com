from django.contrib import admin
from . models import Post, PostImage, Category, Like, Comment, CommentLike, Notification, ThreadModel

class ImageInline(admin.TabularInline):
	model = PostImage
	extra = 0

class CommentInline(admin.TabularInline):
	model = Comment
	extra = 0

class CommentLikeInline(admin.TabularInline):
	model = CommentLike
	extra = 0

class PostAdmin(admin.ModelAdmin):
	fieldsets = [
		(
			None,
			{
				'fields':[
					'id',
					'title',
					'content',
					'category',
					'date_posted',
					'author',
					('liked',
					'num_likes'),
					'num_comments',
				]
			}
		)
	]
	readonly_fields = ['num_likes', 'num_comments', 'id']

	inlines = [ImageInline, CommentInline]
	list_display = ('id', 'title', 'content', 'category', 'date_posted', 'author', 'num_likes', 'num_comments')
	search_fields = ('author__username', 'date_posted', 'title')
	list_per_page = 50

class CommentAdmin(admin.ModelAdmin):
	fieldsets = [
		(
			None,
			{
				'fields':[
					('post',
					'post_id', 'post_author'),
					'is_parent',
					'num_children',
					'body',
					'user',
					'created',
					'id',
					'liked',
					'num_likes'
				]
			}
		)
	]
	readonly_fields = ['created', 'post_id', 'post_author', 'id', 'num_likes', 'is_parent', 'num_children',]

	inlines = [CommentLikeInline] #this doesnt work, use 'liked' field instead
	list_display = ('post', 'post_id', 'post_author', 'is_parent', 'num_children', 'body', 'user', 'created', 'num_likes')
	search_fields = ['id', 'post', 'post_id', 'post_author']
	list_per_page = 50

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Like)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentLike)
admin.site.register(Notification)
admin.site.register(ThreadModel)