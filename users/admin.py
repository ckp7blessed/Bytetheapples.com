from django.contrib import admin
from . models import Profile

class ProfileAdmin(admin.ModelAdmin):

	readonly_fields = ['id', 'register_ip']
	search_fields = ('user__username', 'id', 'register_ip')
	list_per_page = 50

admin.site.register(Profile, ProfileAdmin)