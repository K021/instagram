from django.shortcuts import redirect
from django.urls import reverse

from post.models import Post, PostComment


__all__ = (
    'comment_add',
    'comment_delete',
)


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


def comment_delete(request, post_pk, com_pk):
    if request.method == 'POST':
        comment = PostComment.objects.get(pk=com_pk)
        if request.user == comment.author:
            comment.delete()
    url = request.META['HTTP_REFERER']
    return redirect(f'{url}#post.{post_pk}')
