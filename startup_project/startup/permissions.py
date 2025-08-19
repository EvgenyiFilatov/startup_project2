from django.shortcuts import get_object_or_404, render
from django.core.exceptions import PermissionDenied

from startup.models import Startup, StartupDeveloper


def custom_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return render(request, 'login.html')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_or_owner_required(view_func):
    def wrapper(request, pk, *args, **kwargs):
        startup = get_object_or_404(Startup, pk=pk)
        user = request.user
        if startup.creator == user:
            return view_func(request, pk, *args, **kwargs)
        dev = (
            StartupDeveloper.objects
            .filter(startup=startup, user=user)
            .first()
        )
        if not user.is_authenticated or not dev or dev.role != 'admin':
            raise PermissionDenied

        return view_func(request, pk, *args, **kwargs)
    return wrapper


def owner_required(view_func):
    def wrapper(request, pk, *args, **kwargs):
        startup = get_object_or_404(Startup, pk=pk)
        user = request.user
        if not user.is_authenticated or startup.creator != user:
            raise PermissionDenied
        return view_func(request, pk, *args, **kwargs)
    return wrapper