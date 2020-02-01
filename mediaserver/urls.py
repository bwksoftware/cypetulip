from django.conf.urls import url

from mediaserver.views import (ServeCompanyFiles, ServeOrderFiles,
                               ServePublicFiles, ServeVersionFiles)

__author__ = ''

urlpatterns = [
    url(r"^orders/(?P<hash>[a-zA-Z0-9_.-]+)/(?P<file>([a-zA-Z0-9_.-]|\W)+)$", ServeOrderFiles.as_view(),
        name="order_files"),
    url(r"^company/(?P<hash>[a-zA-Z0-9_.-]+)/(?P<file>([a-zA-Z0-9_.-]|\W)+)$", ServeCompanyFiles.as_view(),
        name="company_files"),
    url(r"^public/(?P<file>[a-zA-Z0-9_.-]+)$", ServePublicFiles.as_view(),
        name="public_files"),
    url(r"^_versions/(?P<file>[a-zA-Z0-9_.-]+)$", ServeVersionFiles.as_view(),
        name="public_thumbnails"),
]
