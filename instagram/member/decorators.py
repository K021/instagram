from functools import wraps

from django.shortcuts import redirect
from django.urls import reverse


def login_required(view_func):
    @wraps(view_func)
    def decorator(*args, **kwargs):
        if args:
            if not args[0].user.is_authenticated():
                url = reverse('member:login')
                if 'pk' in kwargs:
                    url += f'?post_pk={kwargs["pk"]}'
                elif 'post_pk' in args:
                    url += f'?post_pk={kwargs["post_pk"]}'
                return redirect(url)
        return view_func(*args, **kwargs)
    return decorator
