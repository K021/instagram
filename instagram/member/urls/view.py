from django.conf.urls import url

from ..views.auth import signup, login, logout
from ..views.auth_facebook import facebook_login, FrontFacebookLogin
from ..views.profile import profile, profile_update


urlpatterns = [
    url(r'^signup/$', signup, name='signup'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),

    url(r'^facebook-login/$', facebook_login, name='facebook_login'),
    url(r'^front-facebook-login/$', FrontFacebookLogin.as_view(), name='front-facebook-login'),

    url(r'^profile/$', profile, name='profile'),
    url(r'^profile/update/$', profile_update, name='profile_update'),
]
