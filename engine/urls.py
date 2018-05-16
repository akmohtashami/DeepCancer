from django.urls import re_path

from engine.views import *

app_name = 'engine'
urlpatterns = [
    re_path(r'^$', RequestRun.as_view(), name="request_run"),
    re_path(r'^result/(?P<uid>.+)/$', RunResult.as_view(), name="run_result"),
    re_path(r'^result/(?P<uid>.+)/(?P<filename>.+)$', RunOutputDownload.as_view(), name="run_result_file")
]