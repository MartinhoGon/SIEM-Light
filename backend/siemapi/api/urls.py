from django.contrib import admin
from django.urls import path, include
from api.views import *
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
#    path("api/", include("api.urls")),
#    path('admin/', admin.site.urls),
    # path("feeds/", FeedDetail.get_all, name="feed_list")
    # path("feeds/", FeedDetail.get_all, name="feed_list")
    path('feed/', feed.FeedList.as_view()),
    path('feed/<int:pk>/', feed.FeedDetail.as_view()),
    path('category/', category.CategoryList.as_view()),
    path('category/<int:pk>/', category.CategoryDetail.as_view()),
    path('value/', value.ValueList.as_view()),
    path('value/<int:pk>/', value.ValueDetail.as_view()),
    path('alert/', alert.AlertList.as_view()),
    path('alert/<int:pk>/', alert.AlertDetail.as_view()),
]
