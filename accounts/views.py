from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as BaseLoginView
from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

from bugs.models import Bug
from projects.models import Project
from utils.decorators import anonymous_required
from .forms import UserCreationForm, AuthenticationForm


@anonymous_required
def signup(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
            return redirect("login")
        messages.error(request, form.errors)
    return render(request, "registration/signup.html", {"form": form})


@login_required
def dashboard(request):
    projects = Project.objects.filter(
        Q(manager=request.user) | Q(bug__assigned_to=request.user)
    ).distinct()
    bugs = Bug.objects.filter(
        Q(project__manager=request.user) | Q(assigned_to=request.user)
    )
    priority_counts = bugs.aggregate(
        high_priority_bugs=Count("id", filter=Q(priority=Bug.PRIORITY.HIGH)),
        medium_priority_bugs=Count("id", filter=Q(priority=Bug.PRIORITY.MEDIUM)),
        low_priority_bugs=Count("id", filter=Q(priority=Bug.PRIORITY.LOW)),
    )
    status_counts = bugs.aggregate(
        open_status_bugs=Count("id", filter=Q(status=Bug.STATUS.OPEN)),
        inprogress_status_bugs=Count("id", filter=Q(status=Bug.STATUS.IN_PROGRESS)),
        closed_status_bugs=Count("id", filter=Q(status=Bug.STATUS.CLOSED)),
    )
    return render(
        request,
        "accounts/dashboard.html",
        {
            "projects": projects,
            "bugs": bugs,
            "priority_counts": priority_counts,
            "status_counts": status_counts,
        },
    )


@method_decorator(anonymous_required, name="dispatch")
class LoginView(BaseLoginView):
    form_class = AuthenticationForm
