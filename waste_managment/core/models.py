from django.db import models
from django.core.validators import MinValueValidator


class Capacity(models.Model):
    material = models.CharField(
        max_length=100, unique=True
    )

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Mатериалы'

    def __str__(self):
        return self.material


class Storage(models.Model):
    name = models.CharField(
        max_length=200, verbose_name='Название хранилища', unique=True
    )
    capacities = models.ManyToManyField(
        Capacity,
        verbose_name='Вместимость',
        through='StorageCapacity'
    )

    class Meta:
        verbose_name = 'Хранилище'
        verbose_name_plural = 'Хранилища'

    def __str__(self):
        return f'Хранилище {self.name}'


class StorageCapacity(models.Model):
    storage = models.ForeignKey(
        Storage,
        verbose_name='Хранилище',
        on_delete=models.CASCADE,
        related_name='storage_capacities'
    )
    capacity = models.ForeignKey(
        Capacity, on_delete=models.CASCADE,
        verbose_name='Материал',
        related_name='capacity_material'
    )
    amount = models.IntegerField(
        null=True, verbose_name='Текущая заполненность',
        validators=[MinValueValidator(0)],
        error_messages={'validators': 'Количество должно быть больше 0'}
    )
    max_amount = models.IntegerField(
        verbose_name='Максимальная вместимость',
        validators=[MinValueValidator(10)],
        error_messages={
            'validators': 'Минимальная максимальная вместимость - 10'
        }
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['storage', 'capacity'],
                name='unique_storage_capacity'
            )
        ]
        verbose_name = 'Хранилище/вместимость'
        verbose_name_plural = 'Хранилища/вместимости'

    def __str__(self):
        return (
            f'Хранилище {self.storage} заполнено материалом {self.capacity} '
            f'на {self.amount}/{self.max_amount}'
        )


class Organization(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название организации',
        unique=True
    )
    storages = models.ManyToManyField(
        Storage,
        through='OrganizationStorage'
    )
    capacities = models.ManyToManyField(
        Capacity,
        through='OrganizationCapacity'
    )

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return f'Организация {self.name}'


class OrganizationStorage(models.Model):
    organization = models.ForeignKey(
        Organization,
        verbose_name='Организация',
        on_delete=models.CASCADE,
        related_name='organization_storage'
    )
    storage = models.ForeignKey(
        Storage,
        verbose_name='Хранилище',
        on_delete=models.CASCADE
    )
    distance = models.IntegerField(
        verbose_name='Расстояние в км',
        validators=[MinValueValidator(1)],
        error_messages={
            'validators': 'Дистанция не может быть меньше либо равна 0'
        }

    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['organization', 'storage'],
                name='unique_organization_storage'
            )
        ]
        verbose_name = 'Организация/Хранилище'
        verbose_name_plural = 'Организации/Хранилища'

    def __str__(self):
        return (
            f'Расстояние от организации {self.organization} до хранилища '
            f'{self.storage} - {self.distance}'
        )


class OrganizationCapacity(models.Model):
    organization = models.ForeignKey(
        Organization,
        verbose_name='Организация',
        on_delete=models.CASCADE,
        related_name='organization_capacity'
    )
    capacity = models.ForeignKey(
        Capacity,
        verbose_name='Материал',
        on_delete=models.CASCADE
    )
    amount = models.IntegerField(
        null=True, verbose_name='Текущая заполненность',
        validators=[MinValueValidator(0)],
        error_messages={'validators': 'Количество должно быть больше 0'}
    )
    max_amount = models.IntegerField(
        verbose_name='Максимальная вместимость',
        validators=[MinValueValidator(10)],
        error_messages={
            'validators': 'Минимальная максимальная вместимость - 10'
        }
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['organization', 'capacity'],
                name='unique_organization_capacity'
            )
        ]
        verbose_name = 'Организация/Вместимость'
        verbose_name_plural = 'Организации/Вместимости'

    def __str__(self):
        return (
            f'На данный момент в организации {self.organization} '
            f' {self.amount}/{self.max_amount} отходов {self.capacity}'
        )
