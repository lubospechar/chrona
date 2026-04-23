# ... existing code ...
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views import View
import json
from django.core.serializers import serialize
from .models import CadastralParcel

class HomeView(TemplateView):
    template_name = "geodata/home.html"

class ParcelGeoJSONView(View):
    """
    Class-based view that returns all CadastralParcel objects as a GeoJSON FeatureCollection.
    Transforms coordinates from Czech S-JTSK (EPSG:5514) to GPS (EPSG:4326) for Leaflet.
    """
    def get(self, request, *args, **kwargs):
        # Fetch all parcels
        parcels = CadastralParcel.objects.all()

        # Serialize to GeoJSON and specify the target SRID (4326 = GPS)
        geojson_str = serialize(
            'geojson',
            parcels,
            geometry_field='geom',
            srid=4326,
            fields=('shp_id', 'id_2', 'typppd_kod')
        )

        # Convert string back to dictionary for JsonResponse
        geojson_dict = json.loads(geojson_str)

        return JsonResponse(geojson_dict)


class ParcelNeighborsView(View):
    """
    Class-based view that returns a list of IDs of neighboring parcels.
    """


    def get(self, request, pk, *args, **kwargs):
        try:

            parcel = CadastralParcel.objects.get(pk=pk)

            neighbors = CadastralParcel.objects.filter(
                geom__intersects=parcel.geom
            ).exclude(pk=parcel.pk).values_list('pk', flat=True)

            return JsonResponse({'neighbor_ids': list(neighbors)})

        except CadastralParcel.DoesNotExist:
            return JsonResponse({'neighbor_ids': []}, status=404)


class ParcelFloodZoneView(View):
    """
    Vrátí informaci, zda je parcela v záplavové zóně.
    """

    def get(self, request, pk, *args, **kwargs):
        try:
            parcel = CadastralParcel.objects.get(pk=pk)
            in_flood_zone = parcel.is_in_flood_zone()

            flood_zones = []
            if in_flood_zone:
                # Získáme unikátní názvy toků
                flood_zones = list(set(
                    parcel.get_flood_zones()
                    .exclude(naz_tok__isnull=True)
                    .values_list('naz_tok', flat=True)
                ))

            return JsonResponse({
                'in_flood_zone': in_flood_zone,
                'flood_zones': flood_zones
            })

        except CadastralParcel.DoesNotExist:
            return JsonResponse({'error': 'Parcel not found'}, status=404)