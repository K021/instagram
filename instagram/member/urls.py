from django.conf.urls import url

from member.views import signup, login, logout, facebook_login

urlpatterns = [
    url(r'^signup/$', signup, name='signup'),
    url(r'^login/$', login, name='login'),
    url(r'^logout$', logout, name='logout'),
    url(r'^facebook-login/$', facebook_login, name='facebook_login')
]
