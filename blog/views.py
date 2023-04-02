from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from .models import Post, Comment
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
			'date': date,
			'saved': True
		}
	else:
		response = {
			'saved': False
		}

	return JsonResponse(response)
