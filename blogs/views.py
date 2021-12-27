from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import Post
from .forms import PostForm
# Create your views here.

def blogs(request):
    # posts = Post.objects.filter(status = 1)
    posts = Post.objects.all()  
    context = {
        'posts' : posts,
    }
    return render(request, 'blogs/posts.html', context)

def single_post(request, id):

    post = Post.objects.get(pk = id)
    context = {
        'post' : post,
    }
    return render(request, 'blogs/single-post.html', context)

@login_required(login_url = 'login')
def user_posts(request):
    profile = request.user.profile
    posts = profile.post_set.all()
    
    context = {
        'posts' : posts,
    }
    return render(request, 'blogs/user_posts.html', context)

@login_required(login_url = 'login')
def create_post(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user.profile
            instance.save()
            messages.success(request, "New post created Successfully !")
        return redirect('user-posts')


    context = {
        'form' : form,
        'method' : 'New'
    }
    return render(request, 'blogs/post_form.html', context)

@login_required(login_url = 'login')
def edit_post(request, id):
    
    profile = request.user.profile
    try:
        post = profile.post_set.get(pk=id)
    except :
        messages.error(request, "You are not authorised to edit this post")
        return redirect('user-posts')
    
    form = PostForm(instance = post)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance = post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated Successfully !")
        return redirect('user-posts')


    context = {
        'form' : form,
        'method' : 'Update'
    }
    return render(request, 'blogs/post_form.html', context)


@login_required(login_url = 'login')
def delete_post(request, id):
    
    profile = request.user.profile
    try:
        post = profile.post_set.get(pk=id)
    except :
        messages.error(request, "You are not authorised to delete this post")
        return redirect('user-posts')
    
    if request.method == 'POST':
        post.delete()
        messages.info(request, "Post deleted !")
        return redirect('user-posts')


    content = {
        'type': 'post',
        'name' : post.title,
    }
    return render(request, 'confirm_delete.html', content)
