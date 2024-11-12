from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404, get_list_or_404

from users.models import User
from .models import (
    Storage, StorageCapacity, Capacity, Organization,
    OrganizationCapacity, OrganizationStorage
)


class UserSignUpSerializer(UserCreateSerializer):
    organizations = serializers.PrimaryKeyRelatedField(
        read_only=True,
        many=True,
    )

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name', 'password',
            'organizations'
        )


class UserGetSerializer(UserSerializer):
    organizations = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email',
            'organizations'
        )


class StorageCapacitySerializer(serializers.ModelSerializer):
    material = serializers.ReadOnlyField(
        source='capacity.material'
    )
    id = serializers.PrimaryKeyRelatedField(
        queryset=Capacity.objects.all(),
        source='capacity'
    )

    class Meta:
        model = StorageCapacity
        fields = ('id', 'material', 'amount', 'max_amount')


class StorageGetSerializer(serializers.ModelSerializer):
    capacities = StorageCapacitySerializer(
        source='storage_capacities',
        many=True,
        read_only=True
    )
    name = serializers.CharField(read_only=True)

    class Meta:
        model = Storage
        fields = ('id', 'name', 'capacities')


class StorageSerializer(serializers.ModelSerializer):
    capacities = StorageCapacitySerializer(many=True, required=True)

    class Meta:
        model = Storage
        fields = ('id', 'name', 'capacities')

    def validate(self, data):
        capacities = data.get('capacities')
        materials = []
        for i in range(len(capacities)):
            materials.append(capacities[i]['capacity'])
        if len(materials) != len(set(materials)):
            raise ValidationError('Переданы одинаковые материалы')
        for capacity in capacities:
            if capacity['max_amount'] < capacity['amount']:
                raise ValidationError('Превышена максимальная вместимость')
        return data

    def create(self, validated_data):
        capacities = validated_data.pop('capacities')
        name = validated_data.pop('name')
        storage = Storage.objects.create(name=name)
        for capacity in capacities:
            StorageCapacity.objects.create(
                storage=storage,
                amount=capacity['amount'],
                capacity=capacity['capacity'],
                max_amount=capacity['max_amount']
            )
        return storage

    def update(self, instance, validated_data):
        capacities = validated_data.pop('capacities')
        super().update(instance, validated_data)
        instance.capacities.clear()
        for capacity in capacities:
            StorageCapacity.objects.create(
                storage=instance,
                amount=capacity['amount'],
                capacity=capacity['capacity'],
                max_amount=capacity['max_amount']
            )
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        return StorageGetSerializer(
            instance,
            context={'request': request}
        ).data


class CapacitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Capacity
        fields = ('id', 'material')


class OrganizationCapacitySerializer(serializers.ModelSerializer):
    material = serializers.ReadOnlyField(
        source='capacity.material'
    )
    id = serializers.PrimaryKeyRelatedField(
        queryset=Capacity.objects.all(),
        source='capacity'
    )

    class Meta:
        model = OrganizationCapacity
        fields = ('id', 'material', 'amount', 'max_amount')


class OrganizationStorageSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='storage.name')
    id = serializers.PrimaryKeyRelatedField(
        queryset=Storage.objects.all(),
        source='storage'
    )

    class Meta:
        model = OrganizationStorage
        fields = ('id', 'name', 'distance')


class OrganizationGetSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    storages = OrganizationStorageSerializer(
        source='organization_storage',
        many=True,
        read_only=True
        )
    capacities = OrganizationCapacitySerializer(
        source='organization_capacity',
        many=True,
        read_only=True
    )

    class Meta:
        model = Organization
        fields = ('name', 'storages', 'capacities')


class OrganizationSerializer(serializers.ModelSerializer):
    capacities = OrganizationCapacitySerializer(many=True, required=True)
    storages = OrganizationStorageSerializer(many=True)

    class Meta:
        model = Organization
        fields = ('id', 'name', 'storages', 'capacities')

    def validate(self, data):
        capacities = data.get('capacities')
        materials = []
        for i in range(len(capacities)):
            materials.append(capacities[i]['capacity'])
        if len(materials) != len(set(materials)):
            raise ValidationError('Переданы одинаковые материалы')
        for capacity in capacities:
            if capacity['max_amount'] < capacity['amount']:
                raise ValidationError('Превышена максимальная вместимость')
        return data

    def create(self, validated_data):
        capacities = validated_data.get('capacities')
        storages = validated_data.get('storages')
        name = validated_data.get('name')
        organization = Organization.objects.create(name=name)
        for capacity in capacities:
            OrganizationCapacity.objects.create(
                organization=organization,
                capacity=capacity['capacity'],
                amount=capacity['amount'],
                max_amount=capacity['max_amount']
            )
        for storage in storages:
            OrganizationStorage.objects.create(
                organization=organization,
                storage=storage['storage'],
                distance=storage['distance']
            )
        return organization

    def update(self, instance, validated_data):
        capacities = validated_data.pop('capacities')
        storages = validated_data.pop('storages')
        super().update(instance, validated_data)
        instance.capacities.clear()
        instance.storages.clear()
        for capacity in capacities:
            OrganizationCapacity.objects.create(
                organization=instance,
                capacity=capacity['capacity'],
                amount=capacity['amount'],
                max_amount=capacity['max_amount']
            )
        for storage in storages:
            OrganizationStorage.objects.create(
                organization=instance,
                storage=storage['storage'],
                distance=storage['distance']
            )
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        return OrganizationGetSerializer(
            instance,
            context={'request': request}
        ).data


class RecycleSerializer(serializers.ModelSerializer):
    material = serializers.SlugRelatedField(
        queryset=Capacity.objects.all(),
        slug_field='material'
    )
    amount = serializers.IntegerField()

    class Meta:
        model = Organization
        fields = ('material', 'amount')

    def validate(self, data):
        amount = data.get('amount')
        capacity = data.get('material')
        org_capacity = get_object_or_404(
            OrganizationCapacity,
            organization=self.instance,
            capacity=capacity
        )
        if amount <= 0:
            raise ValidationError(
                'Кол-во не может быть меньше либо равно 0!'
            )
        if amount > org_capacity.amount:
            raise ValidationError(
                'Невозможно переработать больше, чем есть в организации!'
            )
        org_storages = get_list_or_404(
            OrganizationStorage.objects.all(),
            organization=self.instance,
            storage__storage_capacities__capacity=capacity
        )
        can_accept = False
        total_delta = 0
        for org_storage in org_storages:
            storage_capacity = get_object_or_404(
                StorageCapacity,
                capacity=capacity,
                storage=org_storage.storage
            )
            delta = storage_capacity.max_amount - storage_capacity.amount
            total_delta += delta
        if amount <= total_delta:
            can_accept = True
        if not can_accept:
            raise ValidationError(
                'Нет доступных хранилищ на указанное кол-во отходов'
            )
        return data

    def update(self, instance, validated_data):
        capacity = validated_data.get('material')
        amount = validated_data.get('amount')
        org_capacity = get_object_or_404(
            OrganizationCapacity,
            organization=instance,
            capacity=capacity
        )
        org_storages = get_list_or_404(
            OrganizationStorage.objects.all().order_by('distance'),
            organization=instance,
            storage__storage_capacities__capacity=capacity
        )
        for org_storage in org_storages:
            storage_capacity = get_object_or_404(
                StorageCapacity,
                capacity=capacity,
                storage=org_storage.storage
            )
            delta = storage_capacity.max_amount - storage_capacity.amount
            if amount <= delta and delta != 0:
                storage_capacity.amount += amount
                org_capacity.amount -= amount
                storage_capacity.save()
                org_capacity.save()
                break
            if delta != 0:
                storage_capacity.amount += delta
                org_capacity.amount -= delta
                amount -= delta
                storage_capacity.save()
                org_capacity.save()
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        return OrganizationGetSerializer(
            instance,
            context={'request': request}
        ).data
