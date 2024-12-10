from django.urls import re_path
from django.conf.urls.static import static
from django.conf import settings
from labdash.views import Dashboard, trigger_button

urlpatterns = [
    re_path(r"^$", Dashboard.as_view()),
    re_path(r"^trigger/(?P<pk>[0-9]+)", trigger_button),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
