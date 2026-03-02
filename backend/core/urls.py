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
    # branch settings
    path(
        "branch/<uuid:branch_id>/settings",
        views.BranchSettingsAPIView.as_view(),
        name="branch-settings",
    ),
    # branch infos
    path(
        "branch/<uuid:branch_id>/infos",
        views.BranchInfoAPIView.as_view(),
        name="branch-infos",
    ),
    # marketing images
    path(
        "branch/<uuid:branch_id>/marketing-images",
        views.MarketingImagesAPIView.as_view(),
        name="marketing-images",
    ),
    path(
        "branch/<uuid:branch_id>/marketing-images/<uuid:marketing_image_id>",
        views.MarketingImageDetailAPIView.as_view(),
        name="marketing-image-detail",
    ),
    # marketing videos
    path(
        "branch/<uuid:branch_id>/marketing-videos",
        views.MarketingVideoAPIView.as_view(),
        name="marketing-videos",
    ),
    path(
        "branch/<uuid:branch_id>/marketing-videos/<uuid:marketing_video_id>",
        views.MarketingVideoDetailAPIView.as_view(),
        name="marketing-video-detail",
    ),
    # service
    path(
        "branch/<uuid:branch_id>/service",
        views.ServiceAPIView.as_view(),
        name="service",
    ),
    path(
        "branch/<uuid:branch_id>/service/<uuid:service_id>",
        views.ServiceDetailAPIView.as_view(),
        name="service-detail",
    ),
    # queue
    path(
        "branch/<uuid:branch_id>/service/<uuid:service_id>/queue",
        views.QueueAPIView.as_view(),
        name="queue",
    ),
    path(
        "branch/<uuid:branch_id>/service/<uuid:service_id>/join",
        views.JoinQueueAPIView.as_view(),
        name="join-queue",
    ),
    path(
        "branch/<uuid:branch_id>/service/<uuid:service_id>/leave",
        views.LeaveQueueAPIView.as_view(),
        name="leave-queue",
    ),
    path(
        "branch/<uuid:branch_id>/service/<uuid:service_id>/call",
        views.CallQueueAPIView.as_view(),
        name="call-queue",
    ),
    path(
        "branch/<uuid:branch_id>/service/<uuid:service_id>/serve",
        views.ServeQueueAPIView.as_view(),
        name="serve-queue",
    ),
]
