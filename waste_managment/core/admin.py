from django.contrib import admin

from .models import (
    Capacity, Storage, StorageCapacity,
    Organization, OrganizationStorage, OrganizationCapacity
)


@admin.register(Capacity)
class CapacityAdmin(admin.ModelAdmin):
    list_display = ('id', 'material')
    search_fields = ('material',)


class StorageCapacityInline(admin.TabularInline):
    model = StorageCapacity
    extra = 1


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    inlines = [StorageCapacityInline]


class OrganizationStorageInline(admin.TabularInline):
    model = OrganizationStorage
    extra = 1


class OrganizationCapacityInline(admin.TabularInline):
    model = OrganizationCapacity
    extra = 1


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    inlines = [OrganizationStorageInline, OrganizationCapacityInline]


@admin.register(StorageCapacity)
class StorageCapacityAdmin(admin.ModelAdmin):
    list_display = ('id', 'storage', 'capacity', 'amount', 'max_amount')
    search_fields = ('storage__name', 'capacity__material')
    list_filter = ('storage', 'capacity')


@admin.register(OrganizationStorage)
class OrganizationStorageAdmin(admin.ModelAdmin):
    list_display = ('id', 'organization', 'storage', 'distance')
    search_fields = ('organization__name', 'storage__name')
    list_filter = ('organization', 'storage')


@admin.register(OrganizationCapacity)
class OrganizationCapacityAdmin(admin.ModelAdmin):
    list_display = ('id', 'organization', 'capacity', 'amount', 'max_amount')
    search_fields = ('organization__name', 'capacity__material')
    list_filter = ('organization', 'capacity')
