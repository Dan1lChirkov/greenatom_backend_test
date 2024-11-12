from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import StorageViewSet, CapacityViewSet, OrganizationViewSet


router = DefaultRouter()
router.register('storages', StorageViewSet, basename='storages')
router.register('capacities', CapacityViewSet, basename='capacities')
router.register('organizations', OrganizationViewSet, basename='organizations')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
