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
    # assign agent to a company
    path(
        "company/<uuid:company_id>/assign-agent",
        views.AssignCompanyAgentAPIView.as_view(),
        name="assign-agent",
    ),
    path(
        "company/<uuid:company_id>/agent/<uuid:user_id>/remove",
        views.RemoveCompanyAgentAPIView.as_view(),
        name="remove-agent",
    ),
    path(
        "company/me",
        views.MyCompanyAPIView.as_view(),
        name="my-company",
    ),
    # payment
    path(
        "company/<uuid:company_id>/payment",
        views.PaymentAPIView.as_view(),
        name="payment",
    ),
    path(
        "company/<uuid:company_id>/payment/<uuid:payment_id>",
        views.PaymentDetailAPIView.as_view(),
        name="payment-detail",
    ),
    # company settings
    path(
        "company/<uuid:company_id>/settings",
        views.CompanySettingsAPIView.as_view(),
        name="company-settings",
    ),
    # company infos
    path(
        "company/<uuid:company_id>/infos",
        views.CompanyInfoAPIView.as_view(),
        name="company-infos",
    ),
    # marketing images
    path(
        "company/<uuid:company_id>/marketing-images",
        views.MarketingImagesAPIView.as_view(),
        name="marketing-images",
    ),
    path(
        "company/<uuid:company_id>/marketing-images/<uuid:marketing_image_id>",
        views.MarketingImageDetailAPIView.as_view(),
        name="marketing-image-detail",
    ),
    # marketing videos
    path(
        "company/<uuid:company_id>/marketing-videos",
        views.MarketingVideoAPIView.as_view(),
        name="marketing-videos",
    ),
    path(
        "company/<uuid:company_id>/marketing-videos/<uuid:marketing_video_id>",
        views.MarketingVideoDetailAPIView.as_view(),
        name="marketing-video-detail",
    ),
    # service
    path(
        "company/<uuid:company_id>/service",
        views.ServiceAPIView.as_view(),
        name="service",
    ),
    path(
        "company/<uuid:company_id>/service/<uuid:service_id>",
        views.ServiceDetailAPIView.as_view(),
        name="service-detail",
    ),
    # queue
    path(
        "company/<uuid:company_id>/service/<uuid:service_id>/queue",
        views.QueueAPIView.as_view(),
        name="queue",
    ),
    path(
        "company/<uuid:company_id>/service/<uuid:service_id>/join",
        views.JoinQueueAPIView.as_view(),
        name="join-queue",
    ),
    path(
        "company/<uuid:company_id>/service/<uuid:service_id>/leave",
        views.LeaveQueueAPIView.as_view(),
        name="leave-queue",
    ),
    path(
        "company/<uuid:company_id>/service/<uuid:service_id>/call",
        views.CallQueueAPIView.as_view(),
        name="call-queue",
    ),
    path(
        "company/<uuid:company_id>/service/<uuid:service_id>/serve",
        views.ServeQueueAPIView.as_view(),
        name="serve-queue",
    ),
]
