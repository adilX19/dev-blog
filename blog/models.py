from django.db import models
from accounts.models import UserAccount
from datetime import datetime
from taggit.managers import TaggableManager
from django.utils.text import slugify

class Post(models.Model):
	author = models.ForeignKey(UserAccount, related_name='posts', on_delete=models.CASCADE)
	title = models.CharField(max_length=500)
	image = models.FileField(upload_to=f"post-images {datetime.now().strftime('%Y-%m-%d')}", null=True, blank=True)
	body = models.TextField()
	slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
	date_published = models.DateTimeField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	tags = TaggableManager()

	def __str__(self):
		return f"{self.title} created by {self.author.username}"

	# overriding save method, to populate slug on title before saving...
	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(Post, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return f"/blog/posts/{self.id}/"

class Comment(models.Model):
	user = models.ForeignKey(UserAccount, related_name='comments', on_delete=models.CASCADE)
	post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
	text = models.TextField()
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"Comment on {self.post.title}"