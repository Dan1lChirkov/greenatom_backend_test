# Generated by Django 4.2.16 on 2024-11-08 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='capacity',
            name='material',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
