from django.conf.urls import include, url

from . import views

app_name = "todo"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^lists/$', views.lists, name='lists'),
    url(r'^lists/(?P<list_id>[\w]+)/delete/$', views.delete_list, name='delete_list'),
    url(r'^lists/(?P<list_id>[\w]+)/items/$', views.lists_items, name='lists_items'),
    url(r'^lists/(?P<list_id>[\w]+)/items/(?P<item_id>[\w]+)/delete/$', views.delete_item, name='delete_item'),
]
