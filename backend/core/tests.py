from django.core.files.uploadedfile import SimpleUploadedFile
import datetime
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from decimal import Decimal
from django.contrib.auth import get_user_model
from .models import (
    Company,
    Branch,
    Payment,
    MarketingImage,
    MarketingVideo,
    BranchInfos,
    Service,
    Queue,
    Payment,
    BranchSettings,
)

# Create your tests here.

User = get_user_model()

# ===========================================
# Company tests
# ===========================================


class CompanyTestCase(APITestCase):
    """
    Company Tpendingest Case
    Test :
    - List company
    - Create company
    - Retrieve company
    - Update company
    - Delete company
    """

    def setUp(self):
        self.user, _ = User.objects.get_or_create(
            email="user@gmail", password="password"
        )
        self.company = Company.objects.create(
            name="Company 1", description="Description 1", user=self.user
        )

    def test_list_company(self):
        url = reverse("company")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_company(self):
        url = reverse("company")
        data = {"name": "Company 2", "description": "Description 2"}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_company(self):
        url = reverse("company-detail", args=[self.company.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_company(self):
        url = reverse("company-detail", args=[self.company.id])
        data = {"name": "Company 1 Updated", "description": "Description 1 Updated"}
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Company 1 Updated")
        self.assertEqual(response.data["description"], "Description 1 Updated")

    def test_delete_company(self):
        url = reverse("company-detail", args=[self.company.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# ===========================================
# Branch tests
# ===========================================


class BranchTestCase(APITestCase):
    """
    Branch Test Case
    Test :
    - List branch
    - Create branch
    - Retrieve branch
    - Update branch
    - Delete branch
    - Disallow update branch
    - Disallow delete branch
    """

    def setUp(self):
        self.user, _ = User.objects.get_or_create(
            email="user@gmail", password="password", phone_number="123456789"
        )
        self.user_2, _ = User.objects.get_or_create(
            email="user_2@gmail", password="password", phone_number="987654321"
        )
        self.company = Company.objects.create(
            name="Company 1", description="Description 1", user=self.user
        )
        self.branch = Branch.objects.create(
            name="Branch 1", description="Description 1", company=self.company
        )

    def test_list_branch(self):
        url = reverse("branch", kwargs={"company_id": self.company.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_branch(self):
        url = reverse("branch", kwargs={"company_id": self.company.id})
        data = {
            "name": "Branch 2",
            "description": "Description 2",
            "company": self.company.id,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_branch(self):
        url = reverse(
            "branch-detail",
            kwargs={"company_id": self.company.id, "branch_id": self.branch.id},
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_disallow_get_branch(self):
        url = reverse(
            "branch-detail",
            kwargs={"company_id": self.company.id, "branch_id": self.branch.id},
        )
        self.client.force_authenticate(user=self.user_2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_disallow_delete_branch(self):
        url = reverse(
            "branch-detail",
            kwargs={"company_id": self.company.id, "branch_id": self.branch.id},
        )
        self.client.force_authenticate(user=self.user_2)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_branch(self):
        url = reverse(
            "branch-detail",
            kwargs={"company_id": self.company.id, "branch_id": self.branch.id},
        )
        data = {
            "name": "Branch 1 Updated",
            "description": "Description 1 Updated",
            "company": self.company.id,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Branch 1 Updated")
        self.assertEqual(response.data["description"], "Description 1 Updated")

    def test_delete_branch(self):
        url = reverse(
            "branch-detail",
            kwargs={"company_id": self.company.id, "branch_id": self.branch.id},
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# =======================================================================
# Payment tests
# =======================================================================


class PaymentTestCase(APITestCase):
    """
    Payment Test Case
    Test :
    - List payment
    - Create payment
    - Retrieve payment
    - Update payment
    - Delete payment
    - Disallow update payment
    - Disallow delete payment
    """

    def setUp(self):
        self.user, _ = User.objects.get_or_create(
            email="user@gmail", password="password"
        )
        self.company = Company.objects.create(
            name="Company 1", description="Description 1", user=self.user
        )
        self.branch = Branch.objects.create(
            name="Branch 1", description="Description 1", company=self.company
        )
        self.payment = Payment.objects.create(
            amount=Decimal(1000.00),
            transaction_id="1234567890",
            branch=self.branch,
            payment_method="mobile_money",
        )

    def test_list_payment(self):
        url = reverse("payment", kwargs={"branch_id": self.branch.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_payment(self):
        url = reverse(
            "payment-detail",
            kwargs={"branch_id": self.branch.id, "payment_id": self.payment.id},
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_payment(self):
        url = reverse(
            "payment-detail",
            kwargs={"branch_id": self.branch.id, "payment_id": self.payment.id},
        )
        data = {"amount": Decimal(1000.00)}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.data["amount"]), Decimal(1000.00))
        self.assertEqual(response.data["status"], "paid")


# ==================================================================
# Branch settings tests
# ==================================================================


class BranchSettingsTestCase(APITestCase):
    """
    Branch Settings Test Case
    Test :
    - Get branch settings
    - Update branch settings
    """

    def setUp(self):
        self.user, _ = User.objects.get_or_create(
            email="user@gmail", password="password", phone_number="123456789"
        )
        self.user_2, _ = User.objects.get_or_create(
            email="user_2@gmail", password="password", phone_number="123456787"
        )
        self.company = Company.objects.create(
            name="Company 1", description="Description 1", user=self.user
        )
        self.branch = Branch.objects.create(
            name="Branch 1", description="Description 1", company=self.company
        )
        self.branch_settings = BranchSettings.objects.create(
            branch=self.branch,
        )

    def test_get_branch_settings(self):
        url = reverse("branch-settings", kwargs={"branch_id": self.branch.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_branch_settings(self):
        url = reverse("branch-settings", kwargs={"branch_id": self.branch.id})
        data = {"voice_style": "woman", "show_info": False}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["voice_style"], "woman")
        self.assertEqual(response.data["show_info"], False)

    def test_disallow_get_branch_settings(self):
        url = reverse("branch-settings", kwargs={"branch_id": self.branch.id})
        self.client.force_authenticate(user=self.user_2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_disallow_update_branch_settings(self):
        url = reverse("branch-settings", kwargs={"branch_id": self.branch.id})
        data = {"voice_style": "woman", "show_info": False}
        self.client.force_authenticate(user=self.user_2)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# =======================================================================
# Branch infos
# =======================================================================


class BranchInfosTestCase(APITestCase):
    """
    Branch Infos Test Case
    Test :
    - Get branch infos
    - Update branch infos
    - Disallow get branch infos
    - Disallow update branch infos
    """

    def setUp(self):
        self.user, _ = User.objects.get_or_create(
            email="user@gmail", password="password", phone_number="123456789"
        )
        self.user_2, _ = User.objects.get_or_create(
            email="user_2@gmail", password="password", phone_number="123456787"
        )
        self.company = Company.objects.create(
            name="Company 1", description="Description 1", user=self.user
        )
        self.branch = Branch.objects.create(
            name="Branch 1", description="Description 1", company=self.company
        )
        self.branch_infos = BranchInfos.objects.create(
            branch=self.branch, title="Test Title", description="Test Description"
        )

    def test_get_branch_infos(self):
        url = reverse("branch-infos", kwargs={"branch_id": self.branch.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_branch_infos(self):
        url = reverse("branch-infos", kwargs={"branch_id": self.branch.id})
        data = {"title": "New Name", "description": "New Description"}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "New Name")
        self.assertEqual(response.data["description"], "New Description")

    def test_disallow_get_branch_infos(self):
        url = reverse("branch-infos", kwargs={"branch_id": self.branch.id})
        self.client.force_authenticate(user=self.user_2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_disallow_update_branch_infos(self):
        url = reverse("branch-infos", kwargs={"branch_id": self.branch.id})
        data = {"title": "New Name", "description": "New Description"}
        self.client.force_authenticate(user=self.user_2)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# =======================================================================
# Marketing images
# =======================================================================


class MarketingImagesTestCase(APITestCase):
    """
    Marketing Images Test Case
    Test :
    - List marketing images
    - Create marketing image
    - Retrieve marketing image
    - Update marketing image
    - Delete marketing image
    - Disallow update marketing image
    - Disallow delete marketing image
    """

    def setUp(self):
        self.user, _ = User.objects.get_or_create(
            email="user@gmail", password="password", phone_number="123456789"
        )
        self.user_2, _ = User.objects.get_or_create(
            email="user_2@gmail", password="password", phone_number="123456787"
        )
        self.company = Company.objects.create(
            name="Company 1", description="Description 1", user=self.user
        )
        self.branch = Branch.objects.create(
            name="Branch 1", description="Description 1", company=self.company
        )
        self.marketing_image = MarketingImage.objects.create(
            branch=self.branch,
            image=SimpleUploadedFile(
                "/backend/assets/images/image.jpeg", b"file_content", "image/jpeg"
            ),
            title="Title 1",
            description="Description 1",
        )

    def test_list_marketing_images(self):
        url = reverse("marketing-images", kwargs={"branch_id": self.branch.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_marketing_image(self):
        url = reverse(
            "marketing-image-detail",
            kwargs={
                "branch_id": self.branch.id,
                "marketing_image_id": self.marketing_image.id,
            },
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_marketing_image(self):
        url = reverse(
            "marketing-image-detail",
            kwargs={
                "branch_id": self.branch.id,
                "marketing_image_id": self.marketing_image.id,
            },
        )
        data = {"title": "New Title"}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "New Title")

    def test_disallow_get_marketing_image(self):
        url = reverse(
            "marketing-image-detail",
            kwargs={
                "branch_id": self.branch.id,
                "marketing_image_id": self.marketing_image.id,
            },
        )
        self.client.force_authenticate(user=self.user_2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_disallow_update_marketing_image(self):
        url = reverse(
            "marketing-image-detail",
            kwargs={
                "branch_id": self.branch.id,
                "marketing_image_id": self.marketing_image.id,
            },
        )
        data = {"title": "New Title"}
        self.client.force_authenticate(user=self.user_2)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_disallow_delete_marketing_image(self):
        url = reverse(
            "marketing-image-detail",
            kwargs={
                "branch_id": self.branch.id,
                "marketing_image_id": self.marketing_image.id,
            },
        )
        self.client.force_authenticate(user=self.user_2)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# =============================================================================
# Marketing video tests
# =============================================================================


class MarketingVideoTestCase(APITestCase):
    """
    Marketing Video Test Case
    Test :
    - List marketing videos
    - Create marketing video
    - Retrieve marketing video
    - Update marketing video
    - Delete marketing video
    - Disallow update marketing video
    - Disallow delete marketing video
    """

    def setUp(self):
        self.user, _ = User.objects.get_or_create(
            email="user@gmail", password="password", phone_number="123456789"
        )
        self.user_2, _ = User.objects.get_or_create(
            email="user_2@gmail", password="password", phone_number="123456787"
        )
        self.company = Company.objects.create(
            name="Company 1", description="Description 1", user=self.user
        )
        self.branch = Branch.objects.create(
            name="Branch 1", description="Description 1", company=self.company
        )
        self.marketing_video = MarketingVideo.objects.create(
            branch=self.branch,
            video=SimpleUploadedFile(
                "/backend/assets/videos/video.mp4", b"file_content", "video/mp4"
            ),
            title="Title 1",
            description="Description 1",
        )

    def test_list_marketing_videos(self):
        url = reverse("marketing-videos", kwargs={"branch_id": self.branch.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_marketing_video(self):
        url = reverse(
            "marketing-video-detail",
            kwargs={
                "branch_id": self.branch.id,
                "marketing_video_id": self.marketing_video.id,
            },
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_marketing_video(self):
        url = reverse(
            "marketing-video-detail",
            kwargs={
                "branch_id": self.branch.id,
                "marketing_video_id": self.marketing_video.id,
            },
        )
        data = {"title": "New Title"}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "New Title")

    def test_disallow_get_marketing_video(self):
        url = reverse(
            "marketing-video-detail",
            kwargs={
                "branch_id": self.branch.id,
                "marketing_video_id": self.marketing_video.id,
            },
        )
        self.client.force_authenticate(user=self.user_2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_disallow_update_marketing_video(self):
        url = reverse(
            "marketing-video-detail",
            kwargs={
                "branch_id": self.branch.id,
                "marketing_video_id": self.marketing_video.id,
            },
        )
        data = {"title": "New Title"}
        self.client.force_authenticate(user=self.user_2)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_disallow_delete_marketing_video(self):
        url = reverse(
            "marketing-video-detail",
            kwargs={
                "branch_id": self.branch.id,
                "marketing_video_id": self.marketing_video.id,
            },
        )
        self.client.force_authenticate(user=self.user_2)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# =============================================================================
# Service tests
# =============================================================================


class ServiceTestCase(APITestCase):
    """
    Service Test Case
    Test :
    - List services
    - Create service
    - Retrieve service
    - Update service
    - Delete service
    - Disallow update service
    - Disallow delete service
    """

    def setUp(self):
        self.user, _ = User.objects.get_or_create(
            email="user@gmail", password="password", phone_number="123456789"
        )
        self.user_2, _ = User.objects.get_or_create(
            email="user_2@gmail", password="password", phone_number="123456787"
        )
        self.company = Company.objects.create(
            name="Company 1", description="Description 1", user=self.user
        )
        self.branch = Branch.objects.create(
            name="Branch 1",
            description="Description 1",
            company=self.company,
            is_active=True,
        )
        self.service = Service.objects.create(
            branch=self.branch,
            name="Service 1",
            description="Description 1",
            daily_limit=100,
            waiting_time=60,
            is_active=True,
        )

    def test_list_services(self):
        url = reverse("service", kwargs={"branch_id": self.branch.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_service(self):
        url = reverse(
            "service-detail",
            kwargs={
                "branch_id": self.branch.id,
                "service_id": self.service.id,
            },
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_service(self):
        url = reverse(
            "service-detail",
            kwargs={
                "branch_id": self.branch.id,
                "service_id": self.service.id,
            },
        )
        data = {"name": "New Name"}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "New Name")

    def test_disallow_get_service(self):
        url = reverse(
            "service-detail",
            kwargs={
                "branch_id": self.branch.id,
                "service_id": self.service.id,
            },
        )
        self.client.force_authenticate(user=self.user_2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_disallow_update_service(self):
        url = reverse(
            "service-detail",
            kwargs={
                "branch_id": self.branch.id,
                "service_id": self.service.id,
            },
        )
        data = {"name": "New Name"}
        self.client.force_authenticate(user=self.user_2)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_disallow_delete_service(self):
        url = reverse(
            "service-detail",
            kwargs={
                "branch_id": self.branch.id,
                "service_id": self.service.id,
            },
        )
        self.client.force_authenticate(user=self.user_2)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# =============================================================================
# Queue tests
# =============================================================================


class QueueTestCase(APITestCase):
    """
    Queue Test Case
    Test :
    - Join queue
    - Leave queue
    """

    def setUp(self):
        self.user, _ = User.objects.get_or_create(
            email="user@gmail", password="password", phone_number="123456789"
        )
        self.user_2, _ = User.objects.get_or_create(
            email="user_2@gmail", password="password", phone_number="123456787"
        )
        self.company = Company.objects.create(
            name="Company 1", description="Description 1", user=self.user
        )
        self.branch = Branch.objects.create(
            name="Branch 1",
            description="Description 1",
            company=self.company,
            is_active=True,
        )
        self.service = Service.objects.create(
            branch=self.branch,
            name="Service 1",
            description="Description 1",
            daily_limit=100,
            waiting_time=60,
            is_active=True,
        )

    def test_join_queue(self):
        url = reverse(
            "join-queue",
            kwargs={
                "branch_id": self.branch.id,
                "service_id": self.service.id,
            },
        )
        self.client.force_authenticate(user=self.user_2)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_leave_queue(self):

        # join the queue
        join_url = reverse(
            "join-queue",
            kwargs={
                "branch_id": self.branch.id,
                "service_id": self.service.id,
            },
        )
        self.client.force_authenticate(user=self.user)
        self.client.post(join_url)

        # leave the queue
        url = reverse(
            "leave-queue",
            kwargs={
                "branch_id": self.branch.id,
                "service_id": self.service.id,
            },
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_call_queue(self):

        # join the queue
        join_url = reverse(
            "join-queue",
            kwargs={
                "branch_id": self.branch.id,
                "service_id": self.service.id,
            },
        )
        self.client.force_authenticate(user=self.user)
        self.client.post(join_url)

        # call the queue
        url = reverse(
            "call-queue",
            kwargs={
                "branch_id": self.branch.id,
                "service_id": self.service.id,
            },
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_serve_queue(self):
        # join the queue
        join_url = reverse(
            "join-queue",
            kwargs={
                "branch_id": self.branch.id,
                "service_id": self.service.id,
            },
        )
        self.client.force_authenticate(user=self.user)
        self.client.post(join_url)

        # call the queue
        call_url = reverse(
            "call-queue",
            kwargs={
                "branch_id": self.branch.id,
                "service_id": self.service.id,
            },
        )
        self.client.force_authenticate(user=self.user)
        self.client.patch(call_url)

        # serve the queue
        url = reverse(
            "serve-queue",
            kwargs={
                "branch_id": self.branch.id,
                "service_id": self.service.id,
            },
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
