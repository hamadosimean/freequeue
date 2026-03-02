import datetime
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from general_settings.permissions import (
    IsUserCompany,
    IsUserBranch,
    IsUserService,
    IsUserPayment,
    IsUserOwner,
    IsUserQueue,
    IsUserBranchAgent,
    IsBranchAgent,
)
from .models import (
    Company,
    Branch,
    BranchInfos,
    BranchAgent,
    MarketingImage,
    MarketingVideo,
    Service,
    Queue,
    Payment,
    BranchSettings,
)
from .serializers import (
    CompanySerializer,
    BranchSerializer,
    BranchInfosSerializer,
    MarketingImageSerializer,
    MarketingVideoSerializer,
    ServiceSerializer,
    QueueSerializer,
    PaymentSerializer,
    BranchSettingsSerializer,
    BranchAgentSerializer,
)
from general_settings.constants import CACHE_TIMEOUT_MINUTES
# Create your views here.


# =======================================================
# Company views
# =======================================================
class CompanyAPIView(APIView):
    """
    Company API View
    GET: Get all companies
    POST: Create a new company
    """

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request):
        companies = cache.get("company:list")
        if not companies:
            companies = Company.objects.all()
            cache.set("company:list", companies, timeout=CACHE_TIMEOUT_MINUTES * 60)
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyDetailAPIView(APIView):
    """
    Company Detail API View
    GET: Get company details
    PUT: Update company details
    DELETE: Delete company

    """

    permission_classes = [IsUserCompany]
    throttle_classes = [UserRateThrottle]

    def get_object(self, company_id):
        cache_key = f"company:{company_id}:user:{self.request.user.id}"
        company = cache.get(cache_key)
        if not company:
            company = get_object_or_404(Company, user=self.request.user, id=company_id)
            cache.set(cache_key, company, timeout=CACHE_TIMEOUT_MINUTES * 60)
        self.check_object_permissions(self.request, company)
        return company

    def get(self, request, company_id):
        company = self.get_object(company_id)
        serializer = CompanySerializer(company)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, company_id):
        company = self.get_object(company_id)
        serializer = CompanySerializer(company, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, company_id):
        company = self.get_object(company_id)
        serializer = CompanySerializer(company, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, company_id):
        company = self.get_object(company_id)
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# =======================================================
# Branch views
# =======================================================
class BranchAPIView(APIView):
    """
    Branch API View
    GET: Get all branches
    POST: Create a new branch
    """

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request, company_id):
        cache_key = f"branch:{company_id}:user:{request.user.id}"
        branches = cache.get(cache_key)
        if not branches:
            branches = Branch.objects.select_related("company").filter(
                company__user=request.user, company_id=company_id
            )
            cache.set(cache_key, branches, timeout=CACHE_TIMEOUT_MINUTES * 60)
        serializer = BranchSerializer(branches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, company_id):
        serializer = BranchSerializer(data=request.data)
        with transaction.atomic():
            if serializer.is_valid(raise_exception=True):
                branch = serializer.save(company_id=company_id)
                Payment.objects.create(branch=branch)

                # create branch infos during branch creation
                BranchInfos.objects.create(
                    branch=branch,
                    title=f"Welcome to {branch.company.name}. Make sure to get your ticket before settling in. We appreciate your patience...",
                )

                # create branch settings during branch creation
                BranchSettings.objects.create(branch=branch)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BranchDetailAPIView(APIView):
    """
    Branch Detail API View
    GET: Get branch details
    PUT: Update branch details
    DELETE: Delete branch

    """

    permission_classes = [IsUserBranch]
    throttle_classes = [UserRateThrottle]

    def get_object(self, company_id, branch_id):
        cache_key = (
            f"branch:{branch_id}:company:{company_id}:user:{self.request.user.id}"
        )
        branch = cache.get(cache_key)
        if not branch:
            branch = get_object_or_404(
                Branch.objects,
                id=branch_id,
                company_id=company_id,
            )
            cache.set(cache_key, branch, timeout=CACHE_TIMEOUT_MINUTES * 60)

        self.check_object_permissions(self.request, branch)
        return branch

    def get(self, request, company_id, branch_id):
        branch = self.get_object(company_id, branch_id)
        serializer = BranchSerializer(branch)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, company_id, branch_id):
        branch = self.get_object(company_id, branch_id)
        serializer = BranchSerializer(branch, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, company_id, branch_id):
        branch = self.get_object(company_id, branch_id)
        serializer = BranchSerializer(branch, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, company_id, branch_id):
        branch = self.get_object(company_id, branch_id)
        branch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ===================================================================
# Agent branch api view
# ==================================================================
class AssignBranchAgentAPIView(APIView):
    """
    Assign agent to a branch
    POST: Assign agent to a branch
    """

    permission_classes = [IsUserBranchAgent]
    throttle_classes = [UserRateThrottle]

    def post(self, request, branch_id):
        serializer = BranchAgentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(branch_id=branch_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveBranchAgentAPIView(APIView):
    """
    Remove agent from a branch
    DELETE: Remove agent from a branch
    """

    permission_classes = [IsUserBranchAgent]
    throttle_classes = [UserRateThrottle]

    def delete(self, request, branch_id, user_id):
        branch_agent = BranchAgent.objects.filter(
            user_id=user_id, branch_id=branch_id
        ).first()
        if not branch_agent:
            return Response(status=status.HTTP_404_NOT_FOUND)
        branch_agent.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyBranchAPIView(APIView):
    """
    My Branch API View
    GET: Get my branch
    """

    throttle_classes = [UserRateThrottle]
    permission_classes = [IsBranchAgent]

    def get(self, request):
        cache_key = f"my-branch:{request.user.id}"
        my_branch = cache.get(cache_key)
        if not my_branch:
            my_branch = BranchAgent.objects.filter(user_id=request.user.id).first()
            cache.set(cache_key, my_branch, timeout=CACHE_TIMEOUT_MINUTES * 60)
        serializer = BranchSerializer(my_branch.branch)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ======================================================================
# Payment api view
# ===================================================================
class PaymentAPIView(APIView):
    """
    Payment API View
    GET: Get all payments

    """

    permission_classes = [IsUserBranch]
    throttle_classes = [UserRateThrottle]

    def get(self, request, branch_id):
        cache_key = f"payment:{branch_id}:user:{request.user.id}"
        payments = cache.get(cache_key)
        if not payments:
            payments = Payment.objects.filter(branch_id=branch_id)
            cache.set(cache_key, payments, timeout=CACHE_TIMEOUT_MINUTES * 60)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PaymentDetailAPIView(APIView):
    """
    Payment API View
    GET: Get payment details
    PATCH: Update payment
    """

    permission_classes = [IsUserPayment]
    throttle_classes = [UserRateThrottle]

    def get_object(self, branch_id, payment_id):
        cache_key = (
            f"payment:{payment_id}:branch:{branch_id}:user:{self.request.user.id}"
        )
        payment = cache.get(cache_key)
        if not payment:
            payment = Payment.objects.filter(id=payment_id, branch_id=branch_id).first()
            cache.set(cache_key, payment, timeout=CACHE_TIMEOUT_MINUTES * 60)
        if not payment:
            return Response(
                {"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND
            )
        self.check_object_permissions(self.request, payment)
        return payment

    def get(self, request, branch_id, payment_id):
        payment = self.get_object(branch_id, payment_id)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, branch_id, payment_id):
        with transaction.atomic():
            payment = self.get_object(branch_id, payment_id)
            branch = payment.branch
            serializer = PaymentSerializer(payment, data=request.data, partial=True)
            if payment.status == "paid":
                return Response(
                    {"error": "Payment has already been made"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if serializer.is_valid(raise_exception=True):
                if Decimal(serializer.validated_data["amount"]) <= Decimal(0):
                    return Response(
                        {"error": "Amount must be greater than 0"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                serializer.validated_data["status"] = "paid"
                serializer.save()
                branch.is_active = True
                branch.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==========================================================================
# branch settings views
# ==========================================================================


class BranchSettingsAPIView(APIView):
    """
    Branch Settings API View
    GET: Get branch settings
    PATCH: Update branch settings
    """

    permission_classes = [IsUserOwner]
    throttle_classes = [UserRateThrottle]

    def get_object(self, branch_id):
        cache_key = f"branch_settings:{branch_id}:user:{self.request.user.id}"
        branch = cache.get(cache_key)
        if not branch:
            branch = BranchSettings.objects.filter(branch_id=branch_id).first()
            cache.set(cache_key, branch, timeout=CACHE_TIMEOUT_MINUTES * 60)
        self.check_object_permissions(self.request, branch)
        return branch

    def get(self, request, branch_id):
        branch = self.get_object(branch_id)
        serializer = BranchSettingsSerializer(branch)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, branch_id):
        branch = self.get_object(branch_id)
        serializer = BranchSettingsSerializer(branch, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==========================================================================
# Branch Infos
# ==========================================================================


class BranchInfoAPIView(APIView):
    """
    Branch Info API View
    GET: Get branch info
    PATCH: Update branch info
    """

    permission_classes = [IsUserOwner]
    throttle_classes = [UserRateThrottle]

    def get_object(self, branch_id):
        cache_key = f"branch_infos:{branch_id}:user:{self.request.user.id}"
        branch = cache.get(cache_key)
        if not branch:
            branch = get_object_or_404(BranchInfos, branch_id=branch_id)
            cache.set(cache_key, branch, timeout=CACHE_TIMEOUT_MINUTES * 60)
        self.check_object_permissions(self.request, branch)
        return branch

    def get(self, request, branch_id):
        branch = self.get_object(branch_id)
        serializer = BranchInfosSerializer(branch)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, branch_id):
        branch = self.get_object(branch_id)
        serializer = BranchInfosSerializer(branch, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==========================================================================
# Marketing images views
# ==========================================================================


class MarketingImagesAPIView(APIView):
    """
    Marketing Images API View
    GET: Get marketing images
    POST: Create marketing image
    """

    permission_classes = [IsUserOwner]
    throttle_classes = [UserRateThrottle]

    def get(self, request, branch_id):
        cache_key = f"marketing_images:{branch_id}:user:{self.request.user.id}"
        marketing_images = cache.get(cache_key)
        if not marketing_images:
            marketing_images = MarketingImage.objects.filter(branch_id=branch_id)
            cache.set(cache_key, marketing_images, timeout=CACHE_TIMEOUT_MINUTES * 60)
        serializer = MarketingImageSerializer(marketing_images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, branch_id):
        serializer = MarketingImageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(branch_id=branch_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MarketingImageDetailAPIView(APIView):
    """
    Marketing Image Detail API View
    GET: Get marketing image details
    PATCH: Update marketing image
    DELETE: Delete marketing image
    """

    permission_classes = [IsUserOwner]
    throttle_classes = [UserRateThrottle]

    def get_object(self, branch_id, marketing_image_id):
        cache_key = f"marketing_image:{marketing_image_id}:branch:{branch_id}:user:{self.request.user.id}"
        marketing_image = cache.get(cache_key)
        if not marketing_image:
            marketing_image = get_object_or_404(
                MarketingImage, id=marketing_image_id, branch_id=branch_id
            )
            cache.set(cache_key, marketing_image, timeout=CACHE_TIMEOUT_MINUTES * 60)
        self.check_object_permissions(self.request, marketing_image)
        return marketing_image

    def get(self, request, branch_id, marketing_image_id):
        marketing_image = self.get_object(branch_id, marketing_image_id)
        serializer = MarketingImageSerializer(marketing_image)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, branch_id, marketing_image_id):
        marketing_image = self.get_object(branch_id, marketing_image_id)
        serializer = MarketingImageSerializer(marketing_image, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, branch_id, marketing_image_id):
        marketing_image = self.get_object(branch_id, marketing_image_id)
        serializer = MarketingImageSerializer(
            marketing_image, data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, branch_id, marketing_image_id):
        marketing_image = self.get_object(branch_id, marketing_image_id)
        marketing_image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# =============================================================================
# Marketing video views
# =============================================================================


class MarketingVideoAPIView(APIView):
    """
    Marketing Video API View
    GET: Get all marketing videos
    POST: Create a new marketing video
    """

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request, branch_id):
        cache_key = f"marketing_videos:{branch_id}:user:{self.request.user.id}"
        marketing_videos = cache.get(cache_key)
        if not marketing_videos:
            marketing_videos = MarketingVideo.objects.filter(branch_id=branch_id)
            cache.set(cache_key, marketing_videos, timeout=CACHE_TIMEOUT_MINUTES * 60)
        serializer = MarketingVideoSerializer(marketing_videos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, branch_id):
        serializer = MarketingVideoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(branch_id=branch_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MarketingVideoDetailAPIView(APIView):
    """
    Marketing Video Detail API View
    GET: Get marketing video details
    PATCH: Update marketing video
    DELETE: Delete marketing video
    """

    permission_classes = [IsUserOwner]
    throttle_classes = [UserRateThrottle]

    def get_object(self, branch_id, marketing_video_id):
        cache_key = f"marketing_video:{marketing_video_id}:branch:{branch_id}:user:{self.request.user.id}"
        marketing_video = cache.get(cache_key)
        if not marketing_video:
            marketing_video = get_object_or_404(
                MarketingVideo, id=marketing_video_id, branch_id=branch_id
            )
            cache.set(cache_key, marketing_video, timeout=CACHE_TIMEOUT_MINUTES * 60)
        self.check_object_permissions(self.request, marketing_video)
        return marketing_video

    def get(self, request, branch_id, marketing_video_id):
        marketing_video = self.get_object(branch_id, marketing_video_id)
        serializer = MarketingVideoSerializer(marketing_video)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, branch_id, marketing_video_id):
        marketing_video = self.get_object(branch_id, marketing_video_id)
        serializer = MarketingVideoSerializer(
            marketing_video, data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, branch_id, marketing_video_id):
        marketing_video = self.get_object(branch_id, marketing_video_id)
        marketing_video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# =============================================================================
# Service API View
# =============================================================================


class ServiceAPIView(APIView):
    """
    Service API View
    GET: Get all services
    POST: Create a new service
    """

    permission_classes = [IsUserService]
    throttle_classes = [UserRateThrottle]

    def get(self, request, branch_id):
        cache_key = f"services:{branch_id}:user:{self.request.user.id}"
        services = cache.get(cache_key)
        if not services:
            services = Service.objects.filter(branch_id=branch_id)
            cache.set(cache_key, services, timeout=CACHE_TIMEOUT_MINUTES * 60)
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, branch_id):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(branch_id=branch_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceDetailAPIView(APIView):
    """
    Service Detail API View
    GET: Get service details
    PATCH: Update service
    DELETE: Delete service
    """

    permission_classes = [IsUserService]
    throttle_classes = [UserRateThrottle]

    def get_object(self, branch_id, service_id):
        cache_key = (
            f"service:{service_id}:branch:{branch_id}:user:{self.request.user.id}"
        )
        service = cache.get(cache_key)
        if not service:
            service = get_object_or_404(Service, id=service_id, branch_id=branch_id)
            cache.set(cache_key, service, timeout=CACHE_TIMEOUT_MINUTES * 60)
        self.check_object_permissions(self.request, service)
        return service

    def get(self, request, branch_id, service_id):
        service = self.get_object(branch_id, service_id)
        serializer = ServiceSerializer(service)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, branch_id, service_id):
        service = self.get_object(branch_id, service_id)
        serializer = ServiceSerializer(service, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(branch_id=branch_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, branch_id, service_id):
        service = self.get_object(branch_id, service_id)
        serializer = ServiceSerializer(service, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(branch_id=branch_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, branch_id, service_id):
        service = self.get_object(branch_id, service_id)
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# =======================================================
# Queue views
# =======================================================
class QueueAPIView(APIView):
    """
    Queue API View
    GET: Get all queues
    POST: Create a new queue
    """

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request, branch_id, service_id):
        cache_key = (
            f"queues:{branch_id}:service:{service_id}:user:{self.request.user.id}"
        )
        queues = cache.get(cache_key)
        if not queues:
            queues = Queue.objects.filter(branch_id=branch_id, service_id=service_id)
            cache.set(cache_key, queues, timeout=CACHE_TIMEOUT_MINUTES * 60)
        serializer = QueueSerializer(queues, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class JoinQueueAPIView(APIView):
    """
    Join Queue API View
    POST: Join a queue
    """

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request, branch_id, service_id):
        with transaction.atomic():
            queue = Queue.objects.filter(
                service__branch_id=branch_id,
                service_id=service_id,
                user=request.user,
                status="waiting",
                date_joined=datetime.date.today(),
            ).first()
            if queue:
                return Response(
                    {"detail": "You are already in the queue"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            last_queue = (
                Queue.objects.filter(
                    service__branch_id=branch_id,
                    service_id=service_id,
                    date_joined=datetime.date.today(),
                )
                .order_by("-queue_number")
                .first()
            )
            if last_queue:
                queue = Queue.objects.create(
                    service_id=service_id,
                    user=request.user,
                    queue_number=last_queue.queue_number + 1,
                )
            else:
                queue = Queue.objects.create(
                    service_id=service_id,
                    user=request.user,
                    queue_number=1,
                )
            queue.refresh_from_db()
            queue = queue.queue_number
        return Response({"queue_number": queue}, status=status.HTTP_200_OK)


class LeaveQueueAPIView(APIView):
    """
    Leave Queue API View
    PATCH: Leave a queue
    """

    permission_classes = [IsUserQueue]
    throttle_classes = [UserRateThrottle]

    def get_object(self, branch_id, service_id):
        queue = (
            Queue.objects.select_for_update()
            .filter(
                service__branch_id=branch_id,
                service_id=service_id,
                user=self.request.user,
                status="waiting",
                date_joined=datetime.date.today(),
            )
            .first()
        )
        if not queue:
            return None
        self.check_object_permissions(self.request, queue)
        return queue

    def patch(self, request, branch_id, service_id):
        with transaction.atomic():
            queue = self.get_object(branch_id, service_id)
            if not queue:
                return Response(
                    {"detail": "You are not in the queue"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            queue.status = "canceled"
            queue.save()
            return Response(status=status.HTTP_200_OK)
        return Response(
            {"detail": "Something went wrong"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


class CallQueueAPIView(APIView):
    """
    Call Queue API View
    PATCH: Call a queue
    """

    # permission_classes = [IsBranchAgent]
    throttle_classes = [UserRateThrottle]

    def get_object(self, branch_id, service_id):
        queue = (
            Queue.objects.select_for_update()
            .filter(
                service__branch_id=branch_id,
                service_id=service_id,
                status="waiting",
                date_joined=datetime.date.today(),
            )
            .order_by("queue_number")
            .first()
        )
        self.check_object_permissions(self.request, queue)
        return queue

    def patch(self, request, branch_id, service_id):
        with transaction.atomic():
            # check if there is called queue
            called_queue = Queue.objects.filter(
                service__branch_id=branch_id,
                service_id=service_id,
                status="called",
                date_joined=datetime.date.today(),
            ).first()
            if called_queue:
                return Response(
                    {"detail": "There is a called queue, please serve it first"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # get the first queue waiting
            queue = self.get_object(branch_id, service_id)
            if not queue:
                return Response(
                    {"detail": "No queue to call"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            queue.status = "called"
            queue.save()
            return Response(status=status.HTTP_200_OK)
        return Response(
            {"detail": "Something went wrong"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


class ServeQueueAPIView(APIView):
    """
    Serve Queue API View
    PATCH: Serve a queue
    """

    # permission_classes = [IsBranchAgent]
    throttle_classes = [UserRateThrottle]

    def get_object(self, branch_id, service_id):
        queue = (
            Queue.objects.select_for_update()
            .filter(
                service__branch_id=branch_id,
                service_id=service_id,
                status="called",
                date_joined=datetime.date.today(),
            )
            .first()
        )
        self.check_object_permissions(self.request, queue)
        return queue

    def patch(self, request, branch_id, service_id):
        with transaction.atomic():
            queue = self.get_object(branch_id, service_id)
            if not queue:
                return Response(
                    {"detail": "No queue to serve"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            queue.status = "served"
            queue.save()
            return Response(status=status.HTTP_200_OK)
        return Response(
            {"detail": "Something went wrong"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
