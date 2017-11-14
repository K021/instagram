from django.conf.urls import url, include

urlpatterns = [
    url(r'^post/', include('post.urls.api', namespace='post')),
    url(r'^member/', include('member.urls.api', namespace='member')),
]
