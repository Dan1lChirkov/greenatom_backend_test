import csv

from django.apps import apps
from django.core.management import BaseCommand


MODELS_FIELDS = {}


class Command(BaseCommand):
    help = 'Создание объекта модели по пути к файлу'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help='file path')
        parser.add_argument('--model_name', type=str, help='model name')
        parser.add_argument(
            '--app_name',
            type=str,
            help='Имя приложения, в котором есть данная модель'
        )

    def handle(self, *args, **options):
        file_path = options['path']
        model = apps.get_model(options['app_name'], options['model_name'])
        with open(file_path, 'rt', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=',')
            for row in reader:
                print(f'Создаем объект с данными: {row}')
                model.objects.create(**row)
                print('Объект создан!')
