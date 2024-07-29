from django.contrib import admin

from accounts.models import User
from .models import Bug


@admin.register(Bug)
class BugAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "project",
        "assigned_to",
        "status",
        "priority",
        "created_at",
        "updated_at",
    )
    list_filter = ["status", "priority", "project"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "assigned_to":
            kwargs["queryset"] = User.objects.filter(role=User.ROLE.DEVELOPER)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
