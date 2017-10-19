from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from post.forms import PostForm
from post.models import Post, PostComment


def post_list(request):
    posts = Post.objects.all()
    contexts = {
        'posts': posts,
    }
    return render(request, 'post/post_list.html', contexts)


def post_detail(request, pk):
    # post = Post.objects.get(pk=pk)
    # get_object_or_404()는 인스턴스가 있으면 가져오고 없으면 404 에러를 호출한다.
    post = get_object_or_404(Post, pk=pk)
    contexts = {
        'post': post,
    }
    return render(request, 'post/post_detail.html', contexts)


def comment_add(request, pk):
    comment = request.POST.get('content')
    PostComment.objects.create(post=Post.objects.get(pk=pk), content=comment)
    contexts = {
        'posts': Post.objects.all()
    }
    url = request.META['HTTP_REFERER']
    return redirect(f'{url}#post.{pk}')


def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            post = Post.objects.create(
                photo=form.cleaned_data['photo'],
                title=form.cleaned_data['title'],
            )
            # return HttpResponse(f'<img src="{post.photo.url}">')
            return redirect('post:detail', pk=post.pk)
    else:
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'post/post_create.html', context)


def post_delete(request, pk):
    if request.method == 'POST':
        Post.objects.get(pk=pk).delete()
        return redirect('main')
    return


def comment_delete(request, post_pk, com_pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=post_pk)
        post.comments.get(pk=com_pk).delete()
    url = request.META['HTTP_REFERER']
    return redirect(f'{url}#post.{post_pk}')

# def post_create(request):
#     photo = request.FILES['photo']
#     if request.method == 'POST' and photo:
#         post = Post.objects.create(photo=photo)
#         return redirect('post_detail', pk=post.pk)
#     post_form = PostForm()
#     contexts = {
#         'form': post_form,
#     }
#     return render(request, 'post/post_create.html', contexts)
