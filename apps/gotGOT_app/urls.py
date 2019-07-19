from django.conf.urls import url
from . import views
                
urlpatterns = [
    url(r'^$', views.index),
    url(r'^reg$', views.reg),
    url(r'^login$', views.log),
    url(r'^dashboard$', views.dashboard),
    url(r'^shows$', views.shows),
    url(r'^new_show$', views.newShow),
    url(r'^createshow$', views.createShow),
    url(r'^movies/(?P<showID>\d+)$', views.showDesc),
    url(r'^shows/delete/(?P<showID>\d+)$', views.delete),
    url(r'^shows/(?P<showID>\d+)$', views.joinEvent),
    url(r'^logout$', views.logout),
]