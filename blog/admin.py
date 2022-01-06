from django.contrib import admin
from . models import Post, PostImage

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
					'date_posted',
					'author'
				]
			}
		)
	]
	inlines = [ImageInline]
	list_display = ('title', 'content', 'date_posted', 'author')
	search_fields = ('author__username', 'date_posted', 'title')

admin.site.register(Post, PostAdmin)

