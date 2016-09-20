from django.conf.urls import url
from django.views.generic import TemplateView

from .views import (
    post_list,
    post_create,
    post_detail,
    post_edit,
    post_delete,
    user_posts,
    )

urlpatterns = [
    url(r'^$', post_list, name='list'),
    url(r'^create/$', post_create, name='create'),
    url(r'^user_posts/$', user_posts, name='user_posts'),
    # url(r'^about/$', post_about, name='about'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^post/(?P<slug>[\w-]+)/$', post_detail, name='detail'),
    url(r'^post/(?P<slug>[\w-]+)/edit/$', post_edit, name='edit'),
    url(r'^post/(?P<slug>[\w-]+)/delete/$', post_delete, name='delete'),
]
