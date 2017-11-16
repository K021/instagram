from django.conf.urls import url

from ..apis import PostList, PostDetail, PostLikeToggle

urlpatterns = [
    url(r'^$', PostList.as_view(), name='list'),
    # 정규표현식으로 url 을 배정할 때에는, 위에 선언한 주소가 다른 것을 먹어버리지 않게 조심해야 한다
    # 아래의 경우, r'^(?P<pk>\d+)/$' 에서 뒤의 $를 빼먹는다면 like-toggle 주소가 인식이 되지 않는다
    url(r'^(?P<pk>\d+)/$', PostDetail.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/like-toggle/', PostLikeToggle.as_view(), name='like-toggle')
]
