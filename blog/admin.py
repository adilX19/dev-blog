from django.contrib import admin
from .models import Post, Comment, CommentReply

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ['title', 'date_published', 'created', 'updated']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ['text', 'updated']

@admin.register(CommentReply)
class CommentReplyAdmin(admin.ModelAdmin):
	list_display = ['reply_by', 'content']