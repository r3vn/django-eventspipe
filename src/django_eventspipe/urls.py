from django.urls import path

from . import views

urlpatterns = [
    path('artifact/<uuid:artifact_id>', views.get_artifact, name="get_artifact"),
]
