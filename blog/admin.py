from django.contrib import admin
from . models import Post, PostImage, Category, Like

# Register your models here.

class ImageInline(admin.TabularInline):
	model = PostImage
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
					'num_likes')
				]
			}
		)
	]
	readonly_fields = ['num_likes']

	inlines = [ImageInline]
	list_display = ('title', 'content', 'category', 'date_posted', 'author', 'num_likes')
	search_fields = ('author__username', 'date_posted', 'title')
	list_per_page = 50

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Like)