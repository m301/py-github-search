from django.conf.urls import url

from app import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^search/$', views.search, name='search'),
    url(r'^get_system_stat/$', views.get_system_stat, name='get_system_stat'),
    url(r'^get_all/$', views.get_all, name='get_all'),
]