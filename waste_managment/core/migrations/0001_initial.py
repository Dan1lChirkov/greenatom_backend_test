# Generated by Django 4.2.16 on 2024-11-06 16:57

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Capacity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.CharField(choices=[('Стекло', 'Стекло'), ('Биоотходы', 'Биоотходы'), ('Пластик', 'Пластик')], max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Название организации')),
            ],
            options={
                'verbose_name': 'Организация',
                'verbose_name_plural': 'Организации',
            },
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Название хранилища')),
            ],
            options={
                'verbose_name': 'Хранилище',
                'verbose_name_plural': 'Хранилища',
            },
        ),
        migrations.CreateModel(
            name='StorageCapacity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(error_messages={'validators': 'Количество должно быть больше 0'}, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Текущая заполненность')),
                ('max_amount', models.IntegerField(error_messages={'validators': 'Минимальная максимальная вместимость - 10'}, validators=[django.core.validators.MinValueValidator(10)], verbose_name='Максимальная вместимость')),
                ('capacity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='capacity_material', to='core.capacity', verbose_name='Материал')),
                ('storage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='storage_capacities', to='core.storage', verbose_name='Хранилище')),
            ],
            options={
                'verbose_name': 'Хранилище/вместимость',
                'verbose_name_plural': 'Хранилища/вместимости',
            },
        ),
        migrations.AddField(
            model_name='storage',
            name='capacities',
            field=models.ManyToManyField(through='core.StorageCapacity', to='core.capacity', verbose_name='Вместимость'),
        ),
        migrations.CreateModel(
            name='OrganizationStorage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.IntegerField(error_messages={'validators': 'Дистанция не может быть меньше либо равна 0'}, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Расстояние в км')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization_storage', to='core.organization', verbose_name='Организация')),
                ('storage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.storage', verbose_name='Хранилище')),
            ],
            options={
                'verbose_name': 'Организация/Хранилище',
                'verbose_name_plural': 'Организации/Хранилища',
            },
        ),
        migrations.CreateModel(
            name='OrganizationCapacity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(error_messages={'validators': 'Количество должно быть больше 0'}, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Текущая заполненность')),
                ('max_amount', models.IntegerField(error_messages={'validators': 'Минимальная максимальная вместимость - 10'}, validators=[django.core.validators.MinValueValidator(10)], verbose_name='Максимальная вместимость')),
                ('capacity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.capacity', verbose_name='Материал')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization_capacity', to='core.organization', verbose_name='Организация')),
            ],
            options={
                'verbose_name': 'Организация/Вместимость',
                'verbose_name_plural': 'Организации/Вместимости',
            },
        ),
        migrations.AddField(
            model_name='organization',
            name='capacities',
            field=models.ManyToManyField(through='core.OrganizationCapacity', to='core.capacity'),
        ),
        migrations.AddField(
            model_name='organization',
            name='storages',
            field=models.ManyToManyField(through='core.OrganizationStorage', to='core.storage'),
        ),
        migrations.AddConstraint(
            model_name='storagecapacity',
            constraint=models.UniqueConstraint(fields=('storage', 'capacity'), name='unique_storage_capacity'),
        ),
        migrations.AddConstraint(
            model_name='organizationstorage',
            constraint=models.UniqueConstraint(fields=('organization', 'storage'), name='unique_organization_storage'),
        ),
        migrations.AddConstraint(
            model_name='organizationcapacity',
            constraint=models.UniqueConstraint(fields=('organization', 'capacity'), name='unique_organization_capacity'),
        ),
    ]
