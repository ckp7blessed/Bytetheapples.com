from django.contrib import admin
from . models import Post, PostImage, Category, Like, Comment

# Register your models here.

class ImageInline(admin.TabularInline):
	model = PostImage
	extra = 0

class CommentInline(admin.TabularInline):
	model = Comment
	extra = 0

class PostAdmin(admin.ModelAdmin):
	fieldsets = [
		(
			None,
			{
				'fields':[
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
	readonly_fields = ['num_likes', 'num_comments']

	inlines = [ImageInline, CommentInline]
	list_display = ('title', 'content', 'category', 'date_posted', 'author', 'num_likes', 'num_comments')
	search_fields = ('author__username', 'date_posted', 'title')
	list_per_page = 50


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Like)
admin.site.register(Comment)