import os
from django.core.management.base import BaseCommand
from django.contrib.gis.utils import LayerMapping
from geodata.models import CadastralParcel, cadastral_parcel_mapping

class Command(BaseCommand):
    help = 'Loads parcel shapefiles into the database'

    def add_arguments(self, parser):
        parser.add_argument('shp_path', type=str, help='Path to the .shp file')

    def handle(self, *args, **options):
        shp_path = options['shp_path']

        if not os.path.exists(shp_path):
            self.stdout.write(self.style.ERROR(f'File not found: {shp_path}'))
            return

        self.stdout.write('Loading data into the database (this might take a while)...')

        # Delete old data to prevent duplicates during testing
        CadastralParcel.objects.all().delete()

        # LayerMapping handles the pairing of SHP columns to PostGIS
        # transform=False -> Do not transform to GPS, keep it in Czech S-JTSK (EPSG:5514)
        lm = LayerMapping(
            CadastralParcel, shp_path, cadastral_parcel_mapping,
            transform=False, encoding='windows-1250' # ČÚZK uses Windows-1250 encoding
        )

        lm.save(strict=True, progress=True)

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {CadastralParcel.objects.count()} parcels!'))