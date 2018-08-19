from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create$', views.create, name='create'),
    url(r'^login$', views.login, name='login'),
    url(r'^travels$', views.travels, name='travels'),
    url(r'^cancel_as_traveler(?P<id>\d+)$', views.cancel_as_traveler, name='cancel_as_traveler'),
    url(r'^cancel_as_planner(?P<id>\d+)$', views.cancel_as_planner, name='cancel_as_planner'),
    url(r'^delete(?P<id>\d+)$', views.delete, name='delete'),
    url(r'^view/(?P<id>\d+)$', views.view, name='view'),
    url(r'^join(?P<id>\d+)$', views.join, name='join'),
    url(r'^add_trip$', views.add_trip, name='add_trip'),
    url(r'^add$', views.add, name='add'),
    url(r'^go_back$', views.go_back, name='go_back'),
    url(r'^logout$', views.logout, name='logout')
]
