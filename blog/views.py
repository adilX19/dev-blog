from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from .models import Post, Comment, CommentReply, SavedPost
from .forms import PostCreationForm

def home_page(request):
	posts = Post.objects.order_by('-date_published')[:5]
	template_name = 'home_page.html'
	context = { 'posts':posts }
	return render(request, template_name, context)

def post_list_view(request):
	posts = request.user.posts.all().order_by('-date_published')
	template_name = 'post_list.html'
	context = { 'posts': posts }
	return render(request, template_name, context)

def saved_posts_view(request):
	posts = request.user.saved_posts.all().order_by('-id')
	template_name = 'post_saved.html'
	context = { 'posts': posts }
	return render(request, template_name, context)

def post_details_view(request, pk):
	post = get_object_or_404(Post, pk=pk)
	template_name = 'post_details.html'
	context = { 'post': post }
	return render(request, template_name, context)

def create_post(request):
	form = PostCreationForm()

	if request.method == "POST":
		form = PostCreationForm(request.POST, request.FILES)
		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.author = request.user
			new_post.save()
			return redirect('blog:home_page')

	template_name = 'post_form.html'
	context = { 'form': form }
	return render(request, template_name, context)

def edit_post(request, post_id):
	post = get_object_or_404(Post, id=post_id)
	form = PostCreationForm(request.POST or None, request.FILES or None, instance=post)

	if request.method == "POST":
		form = PostCreationForm(request.POST or None, request.FILES or None, instance=post)
		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.author = request.user
			new_post.save()
			return redirect('blog:home_page')

	template_name = 'post_form.html'
	context = { 'form': form, 'instance': post }
	return render(request, template_name, context)

def add_comment_view(request, post_id):
	post = get_object_or_404(Post, id=post_id)

	if request.method == "POST" and post:
		comment_text = request.POST["comment"]
		new_comment = Comment(user=request.user, post=post, text=comment_text)
		new_comment.save()

		date = new_comment.updated.strftime("%b. %d, %Y")

		response = {
			'text': comment_text,
			'author': request.user.username,
			'image': request.user.image.url,
			'date': date,
			'saved': True
		}
	else:
		response = {
			'saved': False
		}

	return JsonResponse(response)

def add_reply_to_comment_view(request, comment_id):

	if request.method == 'POST':
		comment = get_object_or_404(Comment, id=comment_id)

		if comment and request.user.is_authenticated:
			reply = CommentReply(
				reply_to=comment,
				reply_by=request.user,
				content=request.POST['reply'],
			)
			reply.save()

			return JsonResponse({
				'reply_id': reply.id,
				'profile_image': reply.reply_by.image.url,
				'full_name': reply.reply_by.full_name,
				'date_created': reply.date_created,
				'content': reply.content,
				'message': 'successfully added reply'
			}, status=200)

	return JsonResponse({"message": "Something went wrong!"}, status=400)


def save_post(request):
	if request.method == 'POST':
		post_id = request.POST.get("post_id", None)
		post = get_object_or_404(Post, id=post_id)

		if post.author != request.user:
			if not SavedPost.objects.filter(author=request.user, post=post).exists():
				SavedPost.objects.create(author=request.user, post=post)
				return JsonResponse({"message": "Post saved to user list"})
		
	return JsonResponse({"message": "Error saving user post"})


def unsave_post(request, post_id):
	post = get_object_or_404(Post, id=post_id)
	if post.author != request.user:
		if SavedPost.objects.filter(author=request.user, post=post).exists():
			SavedPost.objects.create(author=request.user, post=post).delete()
			return JsonResponse({"message": "Post deleted from user list"})
			
	return JsonResponse({"message": "Error deleting user post"})