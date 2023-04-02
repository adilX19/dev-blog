from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
	path('home/', views.home_page, name='home_page'),
	path('posts/', views.post_list_view, name='post_list'),
	path('posts/<int:pk>/', views.post_details_view, name='post_details'),
	path('edit/posts/<int:post_id>/', views.edit_post, name='edit_post'),
	path('create/post/', views.create_post, name='create_post'),
	path('post/<int:post_id>/comment/', views.add_comment_view, name='add_comment'),
]