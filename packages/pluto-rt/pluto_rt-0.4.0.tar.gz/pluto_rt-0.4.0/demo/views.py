import uuid

from django.shortcuts import render

from .tasks import sample_ops_function


def run_demo(request):
    """
    Real-time results display of demo report run
    """
    # come up with a unique-ish queue name. it shouldn't be possible to
    # replicate it by another user (it shouldnt' use a timestamp alone)
    queue_name = f"testqueue_{uuid.uuid4()}"

    # kick off the long running task, passing it the unique queue name
    sample_ops_function.delay(queue_name)

    # pass on the queue name to the results view
    ctx = {
        "queue_name": queue_name,
        # these are only required for polling
        "num_per_gulp": 100,
        "interval_seconds": 3,
    }
    # this can also be passed in to the template using an "include" variable
    if request.GET.get("reverse"):
        ctx["reverse"] = True

    # we normally would just reference the template name directly, this is just to
    # show the two types of message delivery
    tname = "polling.html" if request.META.get("wsgi.version") else "sse.html"
    ctx["template_name"] = f"pluto_rt/{tname}"

    return render(request, "demo/demo.html", ctx)
