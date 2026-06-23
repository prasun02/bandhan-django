from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def requests(request):
    return render(request, "returns/requests.html", {"returns": request.user.returnrequest_set.all() if hasattr(request.user, "returnrequest_set") else []})
