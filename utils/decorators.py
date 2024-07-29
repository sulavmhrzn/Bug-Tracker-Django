from functools import wraps

from django.shortcuts import redirect


def manager_required(func):
    @wraps(func)
    def wrap(request, *args, **kwargs):
        if not request.user.is_manager():
            return redirect("dashboard")
        return func(request, *args, **kwargs)

    return wrap


def anonymous_required(func):
    @wraps(func)
    def wrap(request, *args, **kwargs):
        if not request.user.is_anonymous:
            return redirect("dashboard")
        return func(request, *args, **kwargs)

    return wrap
