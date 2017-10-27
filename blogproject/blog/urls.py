from django.conf.urls import url
from . import views

app_name = 'blog'
urlpatterns = [
    # url(r'^$', views.index, name='index'),
    # 将主页视图函数改写成类函数
    url(r'^$', views.IndexView.as_view(), name='index'),

    # 将 category 视图函数改写为类视图
    url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='Category'),
    # url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),

    # 将archives视图函数改写为类函数
    # url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archivesView.as_view(), name='archives'),

    url(r'^post/(?P<pk>[0-9]+)$', views.detail, name='detail'),
    # url(r'^post/(?P<pk>[0-9]+)$', views.PostDetailView.as_view(), name='detail'),

    # url(r'^tag/(?P<pk>[0-9]+)/$', views.tags, name='tag')
    url(r'^tag/(?P<pk>[0-9]+)/$', views.Tagview.as_view(), name='tag'),

    # 搜索
    # url(r'^search/$', views.search, name='search')
]
