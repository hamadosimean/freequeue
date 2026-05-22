from rest_framework.permissions import BasePermission


class IsUserCompany(BasePermission):
    """
    Permission class to ensure that only the owner of a company can access it.
    """

    def has_permission(self, request, view):
        """Check if the user is authenticated."""
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Check if the requesting user is the owner of the company."""
        return obj.user == request.user


class IsUserService(BasePermission):
    """
    Permission class to ensure that only the owner of the branch's company can access the service.
    """

    def has_permission(self, request, view):
        """Check if the user is authenticated."""
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Check if the requesting user owns the company connected to this service's branch."""
        return obj.company.user == request.user and obj.is_active


class IsUserPayment(BasePermission):
    """
    Permission class to ensure that only the owner of the branch's company can access payment records.
    """

    def has_permission(self, request, view):
        """Check if the user is authenticated."""
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Check if the requesting user owns the company connected to this branch's payments."""
        return obj.company.user == request.user


class IsUserOwner(BasePermission):
    """
    Generic permission class to ensure the user owns the related branch's company.
    """

    def has_permission(self, request, view):
        """Check if the user is authenticated."""
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Check if the requesting user is the owner of the company associated with the branch."""
        return obj.company.user == request.user


class IsUserQueue(BasePermission):
    """
    Permission class to ensure that only the user who created the queue entry can access it.
    """

    def has_permission(self, request, view):
        """Check if the user is authenticated."""
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Check if the requesting user is the owner of the queue entry."""
        return obj.user == request.user


class IsUserCompanyAgent(BasePermission):
    """
    Permission class to ensure that only the user who created the company agent can access it.
    """

    def has_permission(self, request, view):
        """Check if the user is authenticated."""
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Check if the requesting user is the owner of the company agent."""
        return obj.company.user == request.user


class IsCompanyAgent(BasePermission):
    """
    Permission class to ensure that only the company agent can access the branch.
    """

    def has_permission(self, request, view):
        """Check if the user is authenticated."""
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Check if the requesting user is the owner of the company agent."""
        return obj.company.user == request.user and obj.user == request.user
