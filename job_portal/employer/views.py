from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.models import EmployerProfile
from .serializers import EmployerProfileSerializer

class EmployerProfileViewSet(viewsets.ModelViewSet):
    """
    CRUD API for Employer Profiles
    - Only employers can modify their own profile
    - Admins can access all profiles
    """
    queryset = EmployerProfile.objects.all()
    serializer_class = EmployerProfileSerializer
    permission_classes = [IsAuthenticated]  # Requires login

    def perform_create(self, serializer):
        """Ensure an employer can only have one profile"""
        if EmployerProfile.objects.filter(user=self.request.user).exists():
            return Response({"error": "Employer profile already exists"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """Admins see all, Employers see only their profile"""
        if self.request.user.is_staff:
            return EmployerProfile.objects.all()
        return EmployerProfile.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        """Ensure employers can only update their own profile"""
        instance = self.get_object()
        if instance.user != request.user and not request.user.is_staff:
            return Response({"error": "You can only update your own profile"}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Ensure employers can only partially update their own profile"""
        instance = self.get_object()
        if instance.user != request.user and not request.user.is_staff:
            return Response({"error": "You can only update your own profile"}, status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Ensure employers can only delete their own profile"""
        instance = self.get_object()
        if instance.user != request.user and not request.user.is_staff:
            return Response({"error": "You can only delete your own profile"}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
