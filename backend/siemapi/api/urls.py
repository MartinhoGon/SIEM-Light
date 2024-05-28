from django.contrib import admin
from django.urls import path, include
from api.views import *
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
#    path("api/", include("api.urls")),
#    path('admin/', admin.site.urls),
    # path("feeds/", FeedDetail.get_all, name="feed_list")
    # path("feeds/", FeedDetail.get_all, name="feed_list")
    path('feed/', FeedList.as_view()),
    path('feed/<int:pk>/', FeedDetail.as_view()),
    path('category/', CategoryList.as_view()),
    path('category/<int:pk>/', CategoryDetail.as_view()),
    path('value/', ValueList.as_view()),
    path('value/<int:pk>/', ValueDetail.as_view()),
    path('alert/', AlertList.as_view()),
    path('alert/<int:pk>/', AlertDetail.as_view()),
    path('start-listener/', StartListener.as_view()),
    path('stop-listener/', StopListener.as_view()),
    path('start-sniffer/', StartSniffer.as_view()),
    path('stop-sniffer/', StopSniffer.as_view()),
    path('upload-file/', FileUploadView.as_view()),
    path('get-stats/', GetStats.as_view()),
]
