import datetime
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from general_settings.permissions import (
    IsUserCompany,
    IsUserService,
    IsUserPayment,
    IsUserOwner,
    IsUserQueue,
    IsCompanyAgent,
)
from .models import (
    Company,
    CompanyInfos,
    Agent,
    MarketingImage,
    MarketingVideo,
    Service,
    Queue,
    Payment,
    CompanySettings,
)
from .serializers import (
    CompanySerializer,
    CompanyInfosSerializer,
    MarketingImageSerializer,
    MarketingVideoSerializer,
    ServiceSerializer,
    QueueSerializer,
    PaymentSerializer,
    CompanySettingsSerializer,
    AgentSerializer,
)
from general_settings.constants import CACHE_TIMEOUT_MINUTES
from .services import update_service_queues
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




# ===================================================================
# Agent company api view
# ==================================================================
class AssignCompanyAgentAPIView(APIView):
    """
    Assign agent to a company
    POST: Assign agent to a company
    """

    permission_classes = [IsCompanyAgent]
    throttle_classes = [UserRateThrottle]

    def post(self, request, company_id):
        serializer = AgentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(company_id=company_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveCompanyAgentAPIView(APIView):
    """
    Remove agent from a company
    DELETE: Remove agent from a company
    """

    permission_classes = [IsCompanyAgent]
    throttle_classes = [UserRateThrottle]

    def delete(self, request, company_id, user_id):
        agent = Agent.objects.filter(
            user_id=user_id, company_id=company_id
        ).first()
        if not agent:
            return Response(status=status.HTTP_404_NOT_FOUND)
        agent.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyCompanyAPIView(APIView):
    """
    My Company API View
    GET: Get my company
    """

    throttle_classes = [UserRateThrottle]
    permission_classes = [IsCompanyAgent]

    def get(self, request):
        cache_key = f"my-company:{request.user.id}"
        my_company = cache.get(cache_key)
        if not my_company:
            my_company = Company.objects.filter(user_id=request.user.id).first()
            cache.set(cache_key, my_company, timeout=CACHE_TIMEOUT_MINUTES * 60)
        serializer = CompanySerializer(my_company)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ======================================================================
# Payment api view
# ===================================================================
class PaymentAPIView(APIView):
    """
    Payment API View
    GET: Get all payments

    """

    permission_classes = [IsUserCompany]
    throttle_classes = [UserRateThrottle]

    def get(self, request, company_id):
        cache_key = f"payment:{company_id}:user:{request.user.id}"
        payments = cache.get(cache_key)
        if not payments:
            payments = Payment.objects.filter(company_id=company_id)
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

    def get_object(self, company_id, payment_id):
        cache_key = (
            f"payment:{payment_id}:company:{company_id}:user:{self.request.user.id}"
        )
        payment = cache.get(cache_key)
        if not payment:
            payment = Payment.objects.filter(id=payment_id, company_id=company_id).first()
            cache.set(cache_key, payment, timeout=CACHE_TIMEOUT_MINUTES * 60)
        if not payment:
            return Response(
                {"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND
            )
        self.check_object_permissions(self.request, payment)
        return payment

    def get(self, request, company_id, payment_id):
        payment = self.get_object(company_id, payment_id)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, company_id, payment_id):
        with transaction.atomic():
            payment = self.get_object(company_id, payment_id)
            company = payment.company
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
                company.is_active = True
                company.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==========================================================================
# company settings views
# ==========================================================================


class CompanySettingsAPIView(APIView):
    """
    Company Settings API View
    GET: Get company settings
    PATCH: Update company settings
    """

    permission_classes = [IsUserOwner]
    throttle_classes = [UserRateThrottle]

    def get_object(self, company_id):
        cache_key = f"company_settings:{company_id}:user:{self.request.user.id}"
        company_settings = cache.get(cache_key)
        if not company_settings:
            company_settings = CompanySettings.objects.filter(company_id=company_id).first()
            cache.set(cache_key, company_settings, timeout=CACHE_TIMEOUT_MINUTES * 60)
        self.check_object_permissions(self.request, company_settings)
        return company_settings

    def get(self, request, company_id):
        company_settings = self.get_object(company_id)
        serializer = CompanySettingsSerializer(company_settings)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, company_id):
        company_settings = self.get_object(company_id)
        serializer = CompanySettingsSerializer(company_settings, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==========================================================================
# Company Infos
# ==========================================================================


class CompanyInfoAPIView(APIView):
    """
    Company Info API View
    GET: Get company info
    PATCH: Update company info
    """

    permission_classes = [IsUserOwner]
    throttle_classes = [UserRateThrottle]

    def get_object(self, company_id):
        cache_key = f"company_infos:{company_id}:user:{self.request.user.id}"
        company = cache.get(cache_key)
        if not company:
            company = get_object_or_404(CompanyInfos, company_id=company_id)
            cache.set(cache_key, company, timeout=CACHE_TIMEOUT_MINUTES * 60)
        self.check_object_permissions(self.request, company)
        return company

    def get(self, request, company_id):
        company = self.get_object(company_id)
        serializer = CompanyInfosSerializer(company)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, company_id):
        company = self.get_object(company_id)
        serializer = CompanyInfosSerializer(company, data=request.data, partial=True)
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

    def get(self, request, company_id):
        cache_key = f"marketing_images:{company_id}:user:{self.request.user.id}"
        marketing_images = cache.get(cache_key)
        if not marketing_images:
            marketing_images = MarketingImage.objects.filter(company_id=company_id)
            cache.set(cache_key, marketing_images, timeout=CACHE_TIMEOUT_MINUTES * 60)
        serializer = MarketingImageSerializer(marketing_images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, company_id):
        serializer = MarketingImageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(company_id=company_id)
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

    def get_object(self, company_id, marketing_image_id):
        cache_key = f"marketing_image:{marketing_image_id}:company:{company_id}:user:{self.request.user.id}"
        marketing_image = cache.get(cache_key)
        if not marketing_image:
            marketing_image = get_object_or_404(
                MarketingImage, id=marketing_image_id, company_id=company_id
            )
            cache.set(cache_key, marketing_image, timeout=CACHE_TIMEOUT_MINUTES * 60)
        self.check_object_permissions(self.request, marketing_image)
        return marketing_image

    def get(self, request, company_id, marketing_image_id):
        marketing_image = self.get_object(company_id, marketing_image_id)
        serializer = MarketingImageSerializer(marketing_image)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, company_id, marketing_image_id):
        marketing_image = self.get_object(company_id, marketing_image_id)
        serializer = MarketingImageSerializer(marketing_image, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, company_id, marketing_image_id):
        marketing_image = self.get_object(company_id, marketing_image_id)
        serializer = MarketingImageSerializer(
            marketing_image, data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, company_id, marketing_image_id):
        marketing_image = self.get_object(company_id, marketing_image_id)
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

    def get(self, request, company_id):
        cache_key = f"marketing_videos:{company_id}:user:{self.request.user.id}"
        marketing_videos = cache.get(cache_key)
        if not marketing_videos:
            marketing_videos = MarketingVideo.objects.filter(company_id=company_id)
            cache.set(cache_key, marketing_videos, timeout=CACHE_TIMEOUT_MINUTES * 60)
        serializer = MarketingVideoSerializer(marketing_videos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, company_id):
        serializer = MarketingVideoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(company_id=company_id)
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

    def get_object(self, company_id, marketing_video_id):
        cache_key = f"marketing_video:{marketing_video_id}:company:{company_id}:user:{self.request.user.id}"
        marketing_video = cache.get(cache_key)
        if not marketing_video:
            marketing_video = get_object_or_404(
                MarketingVideo, id=marketing_video_id, company_id=company_id
            )
            cache.set(cache_key, marketing_video, timeout=CACHE_TIMEOUT_MINUTES * 60)
        self.check_object_permissions(self.request, marketing_video)
        return marketing_video

    def get(self, request, company_id, marketing_video_id):
        marketing_video = self.get_object(company_id, marketing_video_id)
        serializer = MarketingVideoSerializer(marketing_video)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, company_id, marketing_video_id):
        marketing_video = self.get_object(company_id, marketing_video_id)
        serializer = MarketingVideoSerializer(
            marketing_video, data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, company_id, marketing_video_id):
        marketing_video = self.get_object(company_id, marketing_video_id)
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

    def get(self, request, company_id):
        cache_key = f"services:{company_id}:user:{self.request.user.id}"
        services = cache.get(cache_key)
        if not services:
            services = Service.objects.filter(company_id=company_id)
            cache.set(cache_key, services, timeout=CACHE_TIMEOUT_MINUTES * 60)
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, company_id):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(company_id=company_id)
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

    def get_object(self, company_id, service_id):
        cache_key = (
            f"service:{service_id}:company:{company_id}:user:{self.request.user.id}"
        )
        service = cache.get(cache_key)
        if not service:
            service = get_object_or_404(Service, id=service_id, company_id=company_id)
            cache.set(cache_key, service, timeout=CACHE_TIMEOUT_MINUTES * 60)
        self.check_object_permissions(self.request, service)
        return service

    def get(self, request, company_id, service_id):
        service = self.get_object(company_id, service_id)
        serializer = ServiceSerializer(service)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, company_id, service_id):
        service = self.get_object(company_id, service_id)
        serializer = ServiceSerializer(service, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(company_id=company_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, company_id, service_id):
        service = self.get_object(company_id, service_id)
        serializer = ServiceSerializer(service, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(company_id=company_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, company_id, service_id):
        service = self.get_object(company_id, service_id)
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

    def get(self, request, company_id, service_id):
        cache_key = (
            f"queues:{company_id}:service:{service_id}:user:{self.request.user.id}"
        )
        queues = cache.get(cache_key)
        if not queues:
            queues = Queue.objects.filter(company_id=company_id, service_id=service_id)
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

    def post(self, request, company_id, service_id):
        with transaction.atomic():
            queue = Queue.objects.filter(
                service__company_id=company_id,
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
                    service__company_id=company_id,
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
            queue_number = queue.queue_number
            update_service_queues(service_id=service_id)
        return Response({"queue_number": queue_number}, status=status.HTTP_200_OK)


class LeaveQueueAPIView(APIView):
    """
    Leave Queue API View
    PATCH: Leave a queue
    """

    permission_classes = [IsUserQueue]
    throttle_classes = [UserRateThrottle]

    def get_object(self, company_id, service_id):
        queue = (
            Queue.objects.select_for_update()
            .filter(
                service__company_id=company_id,
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

    def patch(self, request, company_id, service_id):
        with transaction.atomic():
            queue = self.get_object(company_id, service_id)
            if not queue:
                return Response(
                    {"detail": "You are not in the queue"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            queue.status = "canceled"
            queue.save()
            update_service_queues(service_id=service_id)
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

    def get_object(self, company_id, service_id):
        queue = (
            Queue.objects.select_for_update()
            .filter(
                service__company_id=company_id,
                service_id=service_id,
                status="waiting",
                date_joined=datetime.date.today(),
            )
            .order_by("queue_number")
            .first()
        )
        self.check_object_permissions(self.request, queue)
        return queue

    def patch(self, request, company_id, service_id):
        with transaction.atomic():
            # check if there is called queue
            called_queue = Queue.objects.filter(
                service__company_id=company_id,
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
            queue = self.get_object(company_id, service_id)
            if not queue:
                return Response(
                    {"detail": "No queue to call"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            queue.status = "called"
            queue.save()
            update_service_queues(service_id=service_id)
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

    def get_object(self, company_id, service_id):
        queue = (
            Queue.objects.select_for_update()
            .filter(
                service__company_id=company_id,
                service_id=service_id,
                status="called",
                date_joined=datetime.date.today(),
            )
            .first()
        )
        self.check_object_permissions(self.request, queue)
        return queue

    def patch(self, request, company_id, service_id):
        with transaction.atomic():
            queue = self.get_object(company_id, service_id)
            if not queue:
                return Response(
                    {"detail": "No queue to serve"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            queue.status = "served"
            queue.save()
            update_service_queues(service_id=service_id)
            return Response(status=status.HTTP_200_OK)
        return Response(
            {"detail": "Something went wrong"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
