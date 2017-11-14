from django.shortcuts import render, redirect

from member.forms import ProfileForm
from post.models import Post


__all__ = (
    'profile',
    'profile_update',
)


def profile(request):
    if not request.user.is_authenticated:
        return redirect('member:login')
    posts = Post.objects.filter(author=request.user)
    context = {
        'posts': posts,
    }
    return render(request, 'member/profile.html', context)


def profile_update(request):
    user = request.user
    if not user.is_authenticated():
        return redirect('member:login')
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        form.is_valid()
        form.update(user)
        return redirect('member:profile')
    else:
        form = ProfileForm(
            initial={
                'nickname': user.nickname,
                'introduction': user.introduction,
            }
        )
    context = {
        'form': form,
    }
    return render(request, 'member/profile_update.html', context)
