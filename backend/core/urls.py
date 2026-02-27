from django.urls import path
from . import views

urlpatterns = [
    # company
    path("company", views.CompanyAPIView.as_view(), name="company"),
    path(
        "company/<uuid:company_id>",
        views.CompanyDetailAPIView.as_view(),
        name="company-detail",
    ),
    # branch
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
    # payment
    path(
        "branch/<uuid:branch_id>/payment",
        views.PaymentAPIView.as_view(),
        name="payment",
    ),
    path(
        "branch/<uuid:branch_id>/payment/<uuid:payment_id>",
        views.PaymentDetailAPIView.as_view(),
        name="payment-detail",
    ),
]
