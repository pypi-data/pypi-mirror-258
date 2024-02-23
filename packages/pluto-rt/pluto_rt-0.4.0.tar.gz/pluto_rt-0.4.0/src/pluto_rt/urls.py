from django.urls import path
from pluto_rt.views import rt_polling, rt_sse

urlpatterns = [
    # Private API view returns and pops items from named queue
    path("polling/<str:queue_name>", view=rt_polling, name="rt_polling"),
    path("sse/<str:queue_name>", view=rt_sse, name="rt_sse"),
]
