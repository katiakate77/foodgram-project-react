import csv

from pathlib import Path
from foodgram_backend.settings import BASE_DIR
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class DataIsLoaded(Exception):
    """Данные уже были загружены в БД"""
    pass


class Command(BaseCommand):

    help = 'Загрузка списка ингредиентов в БД'

    def handle(self, *args, **options):
        # for local development
        # file_path = Path(BASE_DIR).parent / 'data' / 'ingredients.csv'
        file_path = Path(BASE_DIR) / 'ingredients.csv'
        if Ingredient.objects.exists():
            raise DataIsLoaded('Данные уже загружены')
        with open(file_path, encoding='utf-8') as csv_file:
            ingredients = [
                Ingredient(
                    name=row[0],
                    measurement_unit=row[1]
                )
                for row in csv.reader(csv_file)
            ]
            Ingredient.objects.bulk_create(ingredients)
