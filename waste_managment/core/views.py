from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    Storage, Capacity, Organization
)
from .serializers import (
    StorageSerializer, StorageGetSerializer,
    CapacitySerializer, OrganizationSerializer,
    OrganizationGetSerializer, RecycleSerializer
)
from .permissions import WorkerOrAdminOrReadOnly


class StorageViewSet(viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    permission_classes = (IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return StorageGetSerializer
        return StorageSerializer


class CapacityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Capacity.objects.all()
    serializer_class = CapacitySerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    permission_classes = (WorkerOrAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return OrganizationGetSerializer
        return OrganizationSerializer

    @action(methods=['patch'], detail=True, url_path='recycle')
    def recycle(self, request, pk=None):
        organization = Organization.objects.get(pk=pk)
        serializer = RecycleSerializer(
            organization,
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
