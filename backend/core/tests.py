from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import (
    Company,
    Branch,
    Payment,
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
    Company Test Case
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
