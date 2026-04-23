import os
from django.core.management.base import BaseCommand
from django.contrib.gis.utils import LayerMapping
from geodata.models import FloodZone, flood_zone_mapping

class Command(BaseCommand):
    help = 'Načte shapefile záplavových území do databáze'

    def add_arguments(self, parser):
        parser.add_argument('shp_path', type=str, help='Cesta k .shp souboru')

    def handle(self, *args, **options):
        shp_path = options['shp_path']

        if not os.path.exists(shp_path):
            self.stdout.write(self.style.ERROR(f'Soubor nenalezen: {shp_path}'))
            return

        self.stdout.write('Načítám data záplavových území...')

        # Vymažeme stará data
        FloodZone.objects.all().delete()

        # LayerMapping pro 3D geometrii
        lm = LayerMapping(
            FloodZone, shp_path, flood_zone_mapping,
            transform=False, encoding='utf-8'
        )

        lm.save(strict=True, progress=True)

        self.stdout.write(self.style.SUCCESS(f'Úspěšně načteno {FloodZone.objects.count()} polygonů záplavových území!'))