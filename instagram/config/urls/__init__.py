from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from . import view, api

urlpatterns = [
    url(r'^', include(view)),
    url(r'^api/', include(api, namespace='api')),
]

# media url
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
