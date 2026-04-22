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

# Auto-generated LayerMapping dictionary
cadastral_parcel_mapping = {
    'shp_id': 'ID',
    'id_2': 'ID_2',
    'typppd_kod': 'TYPPPD_KOD',
    'katuze_kod': 'KATUZE_KOD',
    'obec_kod': 'OBEC_KOD',
    'geom': 'POLYGON',
}