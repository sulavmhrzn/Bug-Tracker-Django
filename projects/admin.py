from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "manager",
        "created_at",
        "updated_at",
    )
