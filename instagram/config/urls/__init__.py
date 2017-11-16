from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from utils.apis import SendSMS
from . import view, api

urlpatterns = [
    url(r'^', include(view)),
    url(r'^api/', include(api, namespace='api')),
    url(r'^api/utils/sms/send', SendSMS.as_view()),
]

# media url
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
