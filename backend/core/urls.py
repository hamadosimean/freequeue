from django.urls import path
from . import views

urlpatterns = [
    path("company", views.CompanyAPIView.as_view(), name="company"),
    path(
        "company/<uuid:company_id>",
        views.CompanyDetailAPIView.as_view(),
        name="company-detail",
    ),
    path(
        "company/<uuid:company_id>/branch",
        views.BranchAPIView.as_view(),
        name="branch",
    ),
    path(
        "company/<uuid:company_id>/branch/<uuid:branch_id>",
        views.BranchDetailAPIView.as_view(),
        name="branch-detail",
    ),
]
