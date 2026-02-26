from django.db import transaction
from django.db.models import Q
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from general_settings.permissions import (
    IsUserCompany,
    IsUserBranch,
    IsUserService,
    IsUserPayment,
    IsUserOwner,
    IsUserQueue,
)
from .models import (
    Company,
    Branch,
    BranchInfos,
    MarketingImage,
    Video,
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
    VideoSerializer,
    ServiceSerializer,
    QueueSerializer,
    PaymentSerializer,
    BranchSettingsSerializer,
)
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
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)

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
        company = Company.objects.filter(user=self.request.user, id=company_id).first()
        if not company:
            return Response(
                {"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND
            )
        self.check_object_permissions(self.request, company)
        return company

    def get(self, request, company_id):
        company = self.get_object(company_id)
        serializer = CompanySerializer(company)
        return Response(serializer.data)

    def put(self, request, company_id):
        company = self.get_object(company_id)
        serializer = CompanySerializer(company, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, company_id):
        company = self.get_object(company_id)
        serializer = CompanySerializer(company, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
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
        branches = Branch.objects.select_related("company").filter(
            company__user=request.user, company_id=company_id
        )
        serializer = BranchSerializer(branches, many=True)
        return Response(serializer.data)

    def post(self, request, company_id):
        serializer = BranchSerializer(data=request.data)
        with transaction.atomic():
            if serializer.is_valid(raise_exception=True):
                branch = serializer.save(company_id=company_id)
                Payment.objects.create(branch=branch)
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
        branch = (
            Branch.objects.select_related("company")
            .filter(
                company__user=self.request.user, id=branch_id, company_id=company_id
            )
            .first()
        )
        if not branch:
            return Response(
                {"error": "Branch not found"}, status=status.HTTP_404_NOT_FOUND
            )
        self.check_object_permissions(self.request, branch)
        return branch

    def get(self, request, company_id, branch_id):
        branch = self.get_object(company_id, branch_id)
        serializer = BranchSerializer(branch)
        return Response(serializer.data)

    def put(self, request, company_id, branch_id):
        branch = self.get_object(company_id, branch_id)
        serializer = BranchSerializer(branch, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, company_id, branch_id):
        branch = self.get_object(company_id, branch_id)
        serializer = BranchSerializer(branch, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, company_id, branch_id):
        branch = self.get_object(company_id, branch_id)
        branch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
