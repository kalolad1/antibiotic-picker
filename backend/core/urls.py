from . import views
from django.urls import path

urlpatterns = [
    path("", views.dummy_home, name="dummy_home"),
    path("regimen_search", views.regimen_search, name="regimen_search"),
    path(
        "reference_document/<str:diagnosis>",
        views.reference_document,
        name="reference_document",
    ),
]
