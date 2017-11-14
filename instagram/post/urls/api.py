from django.conf.urls import url

from ..apis import PostList

urlpatterns = [
    url(r'^$', PostList.as_view(), name='post'),
]
