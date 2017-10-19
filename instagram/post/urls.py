from django.conf.urls import url

from post.views import post_list, post_detail, comment_add, post_create, comment_delete, post_delete

urlpatterns = [
    url(r'^$', post_list, name='list'),
    url(r'^(?P<pk>\d+)/$', post_detail, name='detail'),
    url(r'^(?P<pk>\d+)/comment/add/$', comment_add, name='comment_add'),
    url(r'^create/$', post_create, name='create'),
    url(r'^(?P<post_pk>\d+)/comment/(?P<com_pk>\d+)/delete/$', comment_delete, name='comment_delete'),
    url(r'^(?P<pk>\d+)/delete/$', post_delete, name='delete')
]