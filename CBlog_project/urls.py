from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static
from users.forms import CustomAuthForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('accounts/', include('allauth.urls')),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.UserProfileListView.as_view(), name='profile'),
    path('profile/settings', user_views.profile_settings, name='profile_settings'),
    path('profile/followers', user_views.FollowersListView.as_view(), name='followers'),
    path('profile/following', user_views.FollowingListView.as_view(), name='following'),
    path('profile/toggle-follower/<int:pk>/', user_views.ToggleFollower.as_view(), name='toggle_follower'),
    path('profile/toggle-follower/js', user_views.toggle_follower_js, name='toggle_follower_js'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', authentication_form=CustomAuthForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('<int:pk>/account_delete/', user_views.UserDeleteView.as_view(), name='user_confirm_delete'),
    path('password-reset/', 
        auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), 
        name='password_reset'),
     path('password-reset/done', 
        auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), 
        name='password_reset_done'),
     path('password-reset-confirm/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), 
        name='password_reset_confirm'),
     path('password-reset-complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
        name='password_reset_complete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else: 
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = 'users.views.handler400'
handler404 = 'users.views.handler404'
handler500 = 'users.views.handler500'