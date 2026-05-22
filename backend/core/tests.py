from django.core.files.uploadedfile import SimpleUploadedFile
import datetime
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from decimal import Decimal
from django.contrib.auth import get_user_model
from .models import (
    Company,
    CompanyInfos,
    Payment,
    MarketingImage,
    MarketingVideo,
    Service,
    Queue,
    Agent,
    CompanySettings,
)

User = get_user_model()

# ===========================================
# Company tests
# ===========================================

class CompanyTestCase(APITestCase):
    """
    Company Test Case
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


# =======================================================================
# Company agent tests
# =======================================================================

class CompanyAgentTestCase(APITestCase):
    def setUp(self):
        self.user, _ = User.objects.get_or_create(
            email="user@gmail", password="password", phone_number="123456789"
        )
        self.agent, _ = User.objects.get_or_create(
            email="agent@gmail", password="password", phone_number="987654321"
        )
        self.company = Company.objects.create(
            name="Company 1", description="Description 1", user=self.user
        )

    def test_assign_agent(self):
        url = reverse("assign-agent", kwargs={"company_id": self.company.id})
        data = {"user_id": self.agent.id, "company_id": self.company.id}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unassign_agent(self):
        url = reverse("assign-agent", kwargs={"company_id": self.company.id})
        data = {"user_id": self.agent.id, "company_id": self.company.id}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse(
            "remove-agent",
            kwargs={"company_id": self.company.id, "user_id": self.agent.id},
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_my_company(self):
        url = reverse("assign-agent", kwargs={"company_id": self.company.id})
        data = {"user_id": self.agent.id, "company_id": self.company.id}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse("my-company")
        self.client.force_authenticate(user=self.agent)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# =======================================================================
# Payment tests
# =======================================================================

class PaymentTestCase(APITestCase):
    def setUp(self):
        self.user, _ = User.objects.get_or_create(
            email="user@gmail", password="password"
        )
        self.company = Company.objects.create(
            name="Company 1", description="Description 1", user=self.user
        )
        self.payment = Payment.objects.create(
            amount=Decimal(1000.00),
            transaction_id="1234567890",
            company=self.company,
            payment_method="mobile_money",
        )

    def test_list_payment(self):
        url = reverse("payment", kwargs={"company_id": self.company.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_payment(self):
        url = reverse(
            "payment-detail",
            kwargs={"company_id": self.company.id, "payment_id": self.payment.id},
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_payment(self):
        url = reverse(
            "payment-detail",
            kwargs={"company_id": self.company.id, "payment_id": self.payment.id},
        )
        data = {"amount": Decimal(1000.00)}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.data["amount"]), Decimal(1000.00))
        self.assertEqual(response.data["status"], "paid")


# ==================================================================
# Company settings tests
# ==================================================================

class CompanySettingsTestCase(APITestCase):
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
        self.company_settings = CompanySettings.objects.create(
            company=self.company,
        )

    def test_get_company_settings(self):
        url = reverse("company-settings", kwargs={"company_id": self.company.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_company_settings(self):
        url = reverse("company-settings", kwargs={"company_id": self.company.id})
        data = {"voice_style": "woman", "show_info": False}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["voice_style"], "woman")
        self.assertEqual(response.data["show_info"], False)

    def test_disallow_get_company_settings(self):
        url = reverse("company-settings", kwargs={"company_id": self.company.id})
        self.client.force_authenticate(user=self.user_2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_disallow_update_company_settings(self):
        url = reverse("company-settings", kwargs={"company_id": self.company.id})
        data = {"voice_style": "woman", "show_info": False}
        self.client.force_authenticate(user=self.user_2)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# =======================================================================
# Company infos
# =======================================================================

class CompanyInfosTestCase(APITestCase):
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
        self.company_infos = CompanyInfos.objects.create(
            company=self.company, title="Test Title", description="Test Description"
        )

    def test_get_company_infos(self):
        url = reverse("company-infos", kwargs={"company_id": self.company.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_company_infos(self):
        url = reverse("company-infos", kwargs={"company_id": self.company.id})
        data = {"title": "New Name", "description": "New Description"}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "New Name")
        self.assertEqual(response.data["description"], "New Description")

    def test_disallow_get_company_infos(self):
        url = reverse("company-infos", kwargs={"company_id": self.company.id})
        self.client.force_authenticate(user=self.user_2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_disallow_update_company_infos(self):
        url = reverse("company-infos", kwargs={"company_id": self.company.id})
        data = {"title": "New Name", "description": "New Description"}
        self.client.force_authenticate(user=self.user_2)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# =======================================================================
# Marketing images
# =======================================================================

class MarketingImagesTestCase(APITestCase):
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
        self.marketing_image = MarketingImage.objects.create(
            company=self.company,
            image=SimpleUploadedFile(
                "/backend/assets/images/image.jpeg", b"file_content", "image/jpeg"
            ),
            title="Title 1",
            description="Description 1",
        )

    def test_list_marketing_images(self):
        url = reverse("marketing-images", kwargs={"company_id": self.company.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_marketing_image(self):
        url = reverse(
            "marketing-image-detail",
            kwargs={
                "company_id": self.company.id,
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
                "company_id": self.company.id,
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
                "company_id": self.company.id,
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
                "company_id": self.company.id,
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
                "company_id": self.company.id,
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
        self.marketing_video = MarketingVideo.objects.create(
            company=self.company,
            video=SimpleUploadedFile(
                "/backend/assets/videos/video.mp4", b"file_content", "video/mp4"
            ),
            title="Title 1",
            description="Description 1",
        )

    def test_list_marketing_videos(self):
        url = reverse("marketing-videos", kwargs={"company_id": self.company.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_marketing_video(self):
        url = reverse(
            "marketing-video-detail",
            kwargs={
                "company_id": self.company.id,
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
                "company_id": self.company.id,
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
                "company_id": self.company.id,
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
                "company_id": self.company.id,
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
                "company_id": self.company.id,
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
        self.service = Service.objects.create(
            company=self.company,
            name="Service 1",
            code="S1",
            description="Description 1",
            daily_limit=100,
            waiting_time=60,
            is_active=True,
        )

    def test_list_services(self):
        url = reverse("service", kwargs={"company_id": self.company.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_service(self):
        url = reverse(
            "service-detail",
            kwargs={
                "company_id": self.company.id,
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
                "company_id": self.company.id,
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
                "company_id": self.company.id,
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
                "company_id": self.company.id,
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
                "company_id": self.company.id,
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
        self.service = Service.objects.create(
            company=self.company,
            name="Service 1",
            code="S1",
            description="Description 1",
            daily_limit=100,
            waiting_time=60,
            is_active=True,
        )

    def test_join_queue(self):
        url = reverse(
            "join-queue",
            kwargs={
                "company_id": self.company.id,
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
                "company_id": self.company.id,
                "service_id": self.service.id,
            },
        )
        self.client.force_authenticate(user=self.user)
        self.client.post(join_url)

        # leave the queue
        url = reverse(
            "leave-queue",
            kwargs={
                "company_id": self.company.id,
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
                "company_id": self.company.id,
                "service_id": self.service.id,
            },
        )
        self.client.force_authenticate(user=self.user)
        self.client.post(join_url)

        # call the queue
        url = reverse(
            "call-queue",
            kwargs={
                "company_id": self.company.id,
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
                "company_id": self.company.id,
                "service_id": self.service.id,
            },
        )
        self.client.force_authenticate(user=self.user)
        self.client.post(join_url)

        # call the queue
        call_url = reverse(
            "call-queue",
            kwargs={
                "company_id": self.company.id,
                "service_id": self.service.id,
            },
        )
        self.client.force_authenticate(user=self.user)
        self.client.patch(call_url)

        # serve the queue
        url = reverse(
            "serve-queue",
            kwargs={
                "company_id": self.company.id,
                "service_id": self.service.id,
            },
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
