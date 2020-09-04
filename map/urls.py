from django.urls import path
from . import views

urlpatterns = [
    path("w_map/", views.w_map, name="w_map"),
    path("washmap/", views.washmap, name="washmap"),
    path("mymap/", views.mymap, name="mymap"),
    # path("getApi/", views.getApi, name='getApi'),
    # path("mapTest/", views.mapTest, name='mapTest'),
]