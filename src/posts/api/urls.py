from django.conf.urls import url
from .views import (
    PostListAPIView, PostDetailAPIView,
    PostUpdateAPIView, PostDeleteAPIView,
    PostCreateAPIView,
)

urlpatterns = [
    url(r'^post/(?P<slug>[\w-]+)/edit/$', PostUpdateAPIView.as_view(), name='edit'),
    url(r'^post/(?P<slug>[\w-]+)/delete/$', PostDeleteAPIView.as_view(), name='delete'),
    url(r'^post/(?P<slug>[\w-]+)/$', PostDetailAPIView.as_view(), name='detail'),
    url(r'^create/$', PostCreateAPIView.as_view(), name='create'),
    url(r'^$', PostListAPIView.as_view(), name='list'),
    ]
