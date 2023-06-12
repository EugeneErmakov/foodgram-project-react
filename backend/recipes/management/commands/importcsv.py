import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from recipes.models import Ingredient, Tag

DATA_ROOT = os.path.join(settings.BASE_DIR, 'recipes/data')


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            'filename',
            default='ingredients.csv',
            nargs='?',
            type=str
        )

    def handle(self, *args, **options):
        try:
            with open(os.path.join(DATA_ROOT, options['filename']),
                      'r', encoding='utf-8') as f:
                data = csv.reader(f)
                for row in data:
                    name, measurement_unit = row
                    Ingredient.objects.get_or_create(
                        name=name,
                        measurement_unit=measurement_unit
                    )
                print('Load ingredients.csv have successful finished')
        except FileNotFoundError:
            raise CommandError('recipes/data/ingredients.csv is not exist')

        try:
            with open(os.path.join(DATA_ROOT, 'tags.csv'),
                      'r', encoding='utf-8') as f:
                data = csv.reader(f)
                for row in data:
                    name, color, slug = row
                    Tag.objects.get_or_create(
                        name=name,
                        color=color,
                        slug=slug
                    )
                print('Load tags.csv have successful finished')
        except FileNotFoundError:
            raise CommandError('recipes/data/tags.csv is not exist')
