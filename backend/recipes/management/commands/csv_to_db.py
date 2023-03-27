from csv import DictReader

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'load data from csv'

    def handle(self, *args, **options):
        model = Ingredient
        if model.objects.exists():
            print(
                f'В {model.name} уже есть данные, отмена загрузки'
            )
        else:
            with open('backend/media/static/data/ingredients.csv',
                      encoding='utf8', newline='') as csvfile:
                csv_reader = DictReader(csvfile, delimiter=',')
                for row in csv_reader:
                    model.objects.create(**row)
            print('Загрузка завершена')
