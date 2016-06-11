from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^beer_list$', views.beer_list, name='beer_list'),
    url(r'^crunch$', views.crunch, name='crunch'),
]