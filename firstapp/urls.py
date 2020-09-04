from django.urls import path
from . import views

urlpatterns = [
    path("mapping/",views.mapping, name="mapping"),
    path("mappoint/",views.pointing, name="mappoint"),
    path("sahoe/", views.sahoe, name="sahoe"),
    path("geoju/", views.geoju, name="geoju"),
    path("job/", views.job, name="job"),
]