from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page

from .forms import CreateComment, CreatePost
from .models import Comment, Group, Post, User, Follow


#@cache_page(20*1, key_prefix='index_page')
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
    following = (request.user.is_authenticated and 
                 request.user != user and 
                 Follow.objects.filter(follower=request.user, 
                                       author=user).exists()) 
    context = {
        'page_obj': page_obj,
        'posts_count': posts_count,
        'following': following
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, id=post_id)
    user = User.objects.get(username=post.author)
    form = CreateComment(request.POST or None)
    comments = Comment.objects.filter(post=post)
    users_posts_count = Post.objects.filter(author=user).count()
    context = {
        'page_obj': post,
        'users_posts_count': users_posts_count,
        'comments': comments,
        'form': form
    }
    return render(request, template, context)


@csrf_exempt
@login_required
def post_create(request):
    template = 'posts/create_post.html'
    grouplist = Group.objects.all()
    if request.method == 'POST':
        form = CreatePost(
            request.POST or None, 
            files=request.FILES or None, 
            )
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
    form = CreatePost(
            request.POST or None, 
            files=request.FILES or None, 
            instance=post
            )
    if request.method == 'GET':
        if not request.user == post.author:
            return redirect('posts:post_detail', post_id=post_id)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
        return redirect('posts:post_detail', post_id=post_id)
    return render(request, template, {'form': form, 'is_edit': 'is_edit'})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CreateComment(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)

@login_required
def follow_index(request):
    template = 'posts/follow.html'
    posts = Post.objects.filter(author__following__follower=request.user)
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, template, context)

@login_required 
def profile_follow(request, username): 
    author = get_object_or_404(User, username=username) 
    follow_check = Follow.objects.filter(author=author, follower=request.user) 
    if author != request.user and not follow_check.exists(): 
        Follow.objects.create(follower=request.user, author=author) 
    return redirect('posts:profile', username=username) 

@login_required 
def profile_unfollow(request, username): 
    get_object_or_404(Follow, 
                      follower=request.user, 
                      author__username=username).delete() 
    return redirect('posts:profile', username=username)
