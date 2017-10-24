from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from member.decorators import login_required
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


@login_required
def post_like(request, pk):
    user = request.user
    if request.method == 'POST':
        if user.liked_posts.filter(pk=pk).exists():
            user.unlike(Post.objects.get(pk=pk))
        else:
            user.like(Post.objects.get(pk=pk))
    url = request.META['HTTP_REFERER']
    return redirect(f'{url}#post.{pk}')


def comment_add(request, pk):
    if not request.user.is_authenticated():
        url = reverse('member:login') + f'?post_pk={pk}&comment={request.POST["comment"]}'
        return redirect(url)
    comment = request.POST.get('comment')
    PostComment.objects.create(
        post=Post.objects.get(pk=pk),
        content=comment,
        author=request.user,
    )
    url = request.META['HTTP_REFERER']
    return redirect(f'{url}#post.{pk}')


def post_create(request):
    if not request.user.is_authenticated():
        return redirect('member:login')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # ModelForm 을 사용
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            # print(form.cleaned_data)
            # post = Post.objects.create(
            #     photo=form.cleaned_data['photo'],
            #     title=form.cleaned_data['title'],
            #     author=request.user,
            # )
            # return HttpResponse(f'<img src="{post.photo.url}">')
            return redirect('post:detail', pk=post.pk)
    else:
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'post/post_create.html', context)


def post_delete(request, pk):
    url = request.META['HTTP_REFERER']
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        if request.user == post.author:
            post.delete()
            return redirect('main')
        return redirect(f'{url}#post.{pk}')
    return redirect(f'{url}#post.{pk}')


def comment_delete(request, post_pk, com_pk):
    if request.method == 'POST':
        comment = PostComment.objects.get(pk=com_pk)
        if request.user == comment.author:
            comment.delete()
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
