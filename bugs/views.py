from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST

from utils.decorators import manager_required
from .forms import (
    CreateBugForm,
    UpdateBugLifecycleForm,
    BugFilterForm,
    CreateCommentForm,
)
from .models import Bug, Comment


@login_required
@manager_required
def create_bug(request):
    form = CreateBugForm(request.user)
    if request.method == "POST":
        form = CreateBugForm(request.user, request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            send_mail(
                subject="A bug has been assigned to you!",
                message=f"Please refer to your dashboard. {request.build_absolute_uri(reverse("detail_bug", kwargs={"pk": instance.id}))}",
                from_email="admin@bug.com",
                recipient_list=[instance.assigned_to.email],
            )
            messages.success(request, "Bugs created successfully.")
            return redirect(f"{reverse(list_bug)}?project={instance.project.pk}")
        messages.error(request, form.errors)
    return render(request, "bugs/create_bug.html", {"form": form})


@login_required
def list_bug(request):
    if request.user.is_developer():
        bugs = (
            Bug.objects.select_related("assigned_to", "project")
            .filter(assigned_to=request.user)
            .order_by("-created_at")
        )
    else:
        bugs = (
            Bug.objects.select_related("project", "assigned_to")
            .filter(project__manager=request.user)
            .order_by("-created_at")
        )
    bug_filter_form = BugFilterForm(
        initial={
            "project": request.GET.get("project"),
            "priority": request.GET.get("priority"),
            "status": request.GET.get("status"),
        },
    )
    if request.GET.get("project"):
        bugs = bugs.filter(project=request.GET["project"])
    if request.GET.get("priority"):
        bugs = bugs.filter(priority=request.GET["priority"])
    if request.GET.get("status"):
        bugs = bugs.filter(status=request.GET["status"])
    paginator = Paginator(bugs, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "bugs/list_bug.html",
        {"bugs": page_obj, "bug_filter_form": bug_filter_form},
    )


@login_required
def update_bug(request, pk):
    if request.user.is_developer():
        return update_bug_lifecycle(request, pk=pk)
    bug = get_object_or_404(Bug, pk=pk, project__manager=request.user)
    form = CreateBugForm(request.user, instance=bug)

    if request.method == "POST":
        form = CreateBugForm(request.user, request.POST, instance=bug)
        if form.is_valid():
            form.save()
            messages.success(request, "Bugs updated successfully.")
            return redirect("list_bug")
        else:
            messages.error(request, form.errors)
            form = CreateBugForm(request.user, instance=bug)
    return render(request, "bugs/update_bug.html", {"form": form, "bug": bug})


def update_bug_lifecycle(request, pk):
    bug = get_object_or_404(Bug, pk=pk, assigned_to=request.user)
    form = UpdateBugLifecycleForm(instance=bug)

    if request.method == "POST":
        form = UpdateBugLifecycleForm(request.POST, instance=bug)
        if form.is_valid():
            form.save()
            messages.success(request, "Bug updated successfully.")
            return redirect("list_bug")
        else:
            form = UpdateBugLifecycleForm(instance=bug)
    return render(request, "bugs/update_bug_lifecycle.html", {"form": form, "bug": bug})


@manager_required
@login_required
@require_POST
def delete_bug(request, pk):
    bug = get_object_or_404(Bug, pk=pk, project__manager=request.user)
    bug.delete()
    messages.success(request, "Bugs deleted successfully.")
    return redirect("list_bug")


@login_required
def detail_bug(request, pk):
    bug = get_object_or_404(Bug, pk=pk)
    comments = Comment.objects.select_related("user").filter(bug=bug)
    comment_form = CreateCommentForm()
    if request.method == "POST":
        comment_form = CreateCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.bug = bug
            comment.user = request.user
            comment.save()
            messages.success(request, "Your comment has been posted successfully.")
            return redirect(reverse("detail_bug", kwargs={"pk": pk}))
        else:
            messages.error(request, comment_form.errors)
            return redirect(reverse("detail_bug", kwargs={"pk": pk}))
    return render(
        request,
        "bugs/detail_bug.html",
        {
            "bug": bug,
            "comment_form": comment_form,
            "comments": comments,
        },
    )
