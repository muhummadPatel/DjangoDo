from django.conf.urls import include, url
from django.views.generic.base import TemplateView
import os

from . import views

app_name = "todo"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^lists/$', views.lists, name='lists'),
    url(r'^lists/(?P<list_id>[\w]+)/delete/$', views.delete_list, name='delete_list'),
    url(r'^lists/(?P<list_id>[\w]+)/items/$', views.lists_items, name='lists_items'),
    url(r'^lists/(?P<list_id>[\w]+)/items/(?P<item_id>[\w]+)/$', views.edit_item, name='edit_items'),
    url(r'^lists/(?P<list_id>[\w]+)/items/(?P<item_id>[\w]+)/delete/$', views.delete_item, name='delete_item'),
]


# to help test 400, and 500 templates during dev
if not os.environ.get('PROD'):
    urlpatterns += (
        url(r'^404/$', TemplateView.as_view(template_name='404.html'), name='test404'),
        url(r'^500/$', TemplateView.as_view(template_name='500.html'), name='test500'),
    )
