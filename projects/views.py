from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from bugs.models import Bug
from utils.decorators import manager_required
from .forms import CreateProjectForm
from .models import Project


@login_required
@manager_required
def create_project(request):
    form = CreateProjectForm()
    if request.method == "POST":
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.manager = request.user
            project.save()
            messages.success(request, "Project created successfully")
            return redirect("dashboard")
        messages.error(request, form.errors)
    return render(request, "projects/create_project.html", {"form": form})


@login_required
def list_projects(request):
    projects = Project.objects.filter(manager=request.user)
    if request.user.is_developer():
        projects = Project.objects.filter(bug__assigned_to=request.user).distinct()
    print(projects)
    return render(request, "projects/list_project.html", {"projects": projects})


@login_required
def detail_project(request, pk):
    project = Project.objects.select_related("manager")
    if request.user.is_manager():
        project = project.filter(Q(manager=request.user)).get(pk=pk)
    if request.user.is_developer():
        project = project.filter(Q(bug__assigned_to=request.user)).get(pk=pk)
    bugs = project.bug.all()
    priority_counts = bugs.aggregate(
        high_priority_bugs=Count("id", filter=Q(priority=Bug.PRIORITY.HIGH)),
        medium_priority_bugs=Count("id", filter=Q(priority=Bug.PRIORITY.MEDIUM)),
        low_priority_bugs=Count("id", filter=Q(priority=Bug.PRIORITY.LOW)),
    )
    bugs = bugs.order_by("updated_at")[:3]
    return render(
        request,
        "projects/detail_project.html",
        {
            "project": project,
            "bugs": bugs,
            "priority_counts": priority_counts,
        },
    )


@login_required
@manager_required
def update_project(request, pk):
    project = get_object_or_404(Project, pk=pk, manager=request.user)
    form = CreateProjectForm(instance=project)
    if request.method == "POST":
        form = CreateProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated successfully")
            return redirect("detail_project", pk=project.pk)
        messages.error(request, form.errors)
    return render(
        request, "projects/update_project.html", {"project": project, "form": form}
    )


@login_required
@manager_required
@require_POST
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk, manager=request.user)
    project.delete()
    messages.success(request, "Project deleted successfully")
    return redirect("dashboard")
