from django.urls import path

from . import views

urlpatterns = [
    path("", views.list_projects, name="list_projects"),
    path("create/", views.create_project, name="create_project"),
    path("<int:pk>/", views.detail_project, name="detail_project"),
    path("<int:pk>/update", views.update_project, name="update_project"),
    path("<int:pk>/delete", views.delete_project, name="delete_project"),
]
