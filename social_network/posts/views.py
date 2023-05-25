from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, User
from django.core.paginator import Paginator
from .forms import CreatePost
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


def index(request):
    template = 'posts/index.html'
    posts = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, template, context)


def posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    user = User.objects.get(username=username)
    posts = Post.objects.filter(author=user)
    posts_count = posts.count()
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'posts_count': posts_count
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = Post.objects.get(id=post_id)
    user = User.objects.get(username=post.author)
    users_posts_count = Post.objects.filter(author=user).count()
    context = {
        'post': post,
        'users_posts_count': users_posts_count
    }
    return render(request, template, context)


@csrf_exempt
@login_required
def post_create(request):
    template = 'posts/create_post.html'
    grouplist = Group.objects.all()
    if request.method == 'POST':
        form = CreatePost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', username=request.user)
    else:
        form = CreatePost()
    return render(request, template, {'form': form, 'grouplist': grouplist})


@csrf_exempt
@login_required
def post_edit(request, post_id):
    template = 'posts/edit_post.html'
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'GET':
        if not request.user == post.author:
            return redirect('posts:post_detail', post_id=post_id)
        form = CreatePost(instance=post)
    if request.method == 'POST':
        form = CreatePost(request.POST, instance=post)
        if form.is_valid():
            form.save()
        return redirect('posts:post_detail', post_id=post_id)
    return render(request, template, {'form': form, 'is_edit': 'is_edit'})
