from django.urls import include, path

from .views import run_demo

urlpatterns = [
    # we are specifying our own template location rather than "pluto_rt/item.html"
    path("rt_messages/", include("pluto_rt.urls"), {"item_template": "demo/pluto_rt_item.html"}),
    path("", run_demo),
]
