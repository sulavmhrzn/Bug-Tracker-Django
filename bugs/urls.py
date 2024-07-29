from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.create_bug, name="create_bug"),
    path("list/", views.list_bug, name="list_bug"),
    path("<int:pk>/", views.detail_bug, name="detail_bug"),
    path("update/<int:pk>/", views.update_bug, name="update_bug"),
    path("delete/<int:pk>/", views.delete_bug, name="delete_bug"),
]
