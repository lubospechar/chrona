from django.contrib.gis.db import models

class CadastralParcel(models.Model):
    shp_id = models.CharField(max_length=40, null=True, blank=True)
    id_2 = models.CharField(max_length=40, null=True, blank=True)
    typppd_kod = models.CharField(max_length=40, null=True, blank=True)
    katuze_kod = models.IntegerField(null=True, blank=True)
    obec_kod = models.IntegerField(null=True, blank=True)

    geom = models.PolygonField(srid=5514)

    def __str__(self):
        return f"Parcela {self.shp_id} (KÚ: {self.katuze_kod})"

    def is_in_flood_zone(self):
        return FloodZone.objects.filter(geom__intersects=self.geom).exists()

    def get_flood_zones(self):
        return FloodZone.objects.filter(geom__intersects=self.geom)

# Auto-generated LayerMapping dictionary
cadastral_parcel_mapping = {
    'shp_id': 'ID',
    'id_2': 'ID_2',
    'typppd_kod': 'TYPPPD_KOD',
    'katuze_kod': 'KATUZE_KOD',
    'obec_kod': 'OBEC_KOD',
    'geom': 'POLYGON',
}


class FloodZone(models.Model):
    tok_id = models.FloatField(null=True, blank=True)
    naz_tok = models.CharField(max_length=60, null=True, blank=True)
    idvt = models.FloatField(null=True, blank=True)
    tokrec_id = models.FloatField(null=True, blank=True)
    rec_naz = models.CharField(max_length=60, null=True, blank=True)
    max_utokjn = models.FloatField(null=True, blank=True)


    geom = models.MultiPolygonField(srid=5514, dim=3)

    def __str__(self):
        return f"Záplavové území: {self.naz_tok or 'Neznámé'}"

flood_zone_mapping = {
    'tok_id': 'TOK_ID',
    'naz_tok': 'NAZ_TOK',
    'idvt': 'IDVT',
    'tokrec_id': 'TOKREC_ID',
    'rec_naz': 'REC_NAZ',
    'max_utokjn': 'MAX_UTOKJN',
    'geom': 'MULTIPOLYGON',
}