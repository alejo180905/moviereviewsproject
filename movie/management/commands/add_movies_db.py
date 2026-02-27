from django.core.management.base import BaseCommand
from django.conf import settings
from movie.models import Movie
import json
import os

class Command(BaseCommand):
    help = 'Carga películas desde movies.json (hasta N)'

    def add_arguments(self, parser):
        parser.add_argument('--json', type=str, default=os.path.join(settings.BASE_DIR, 'movies.json'))
        parser.add_argument('--limit', type=int, default=100)
        parser.add_argument('--clear', action='store_true', help='Eliminar películas existentes antes de cargar')

    def handle(self, *args, **options):
        json_path = options['json']
        limit = options['limit']
        clear = options['clear']

        if clear:
            self.stdout.write('Eliminando películas existentes...')
            Movie.objects.all().delete()

        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f'No se encuentra {json_path}'))
            return

        with open(json_path, encoding='utf-8') as f:
            data = json.load(f)

        count = 0
        for item in data[:limit]:
            title = (item.get('title') or '')[:100]
            genre = (item.get('genre') or '')[:50]
            year_raw = item.get('year', '')
            try:
                year = int(year_raw) if year_raw else None
            except:
                year = None
            description = (item.get('description') or '')[:250]

            # Crear si no existe por título
            obj, created = Movie.objects.get_or_create(
                title=title,
                defaults={
                    'genre': genre,
                    'year': year,
                    'description': description,
                    'image': 'movie/images/default.jpg',
                }
            )
            if created:
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Cargadas {count} películas (de hasta {limit})'))
