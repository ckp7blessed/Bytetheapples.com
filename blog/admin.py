from django.contrib import admin
from . models import Post, PostImage, Category

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
					'author'
				]
			}
		)
	]
	inlines = [ImageInline]
	list_display = ('title', 'content', 'category', 'date_posted', 'author')
	search_fields = ('author__username', 'date_posted', 'title')
	list_per_page = 50

admin.site.register(Post, PostAdmin)
admin.site.register(Category)