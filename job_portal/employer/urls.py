
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployerProfileViewSet

router = DefaultRouter()
#crud for employers
router.register(r'profile', EmployerProfileViewSet)

urlpatterns = [
    path('', include(router.urls)), 
]
