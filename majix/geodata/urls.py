from django.urls import path
from .views import HomeView, ParcelGeoJSONView, ParcelNeighborsView, ParcelFloodZoneView

app_name = "geodata"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("api/parcels/", ParcelGeoJSONView.as_view(), name="api_parcels"),
    path("api/parcels/<int:pk>/neighbors/", ParcelNeighborsView.as_view(), name="api_parcel_neighbors"),
    path("api/parcels/<int:pk>/flood_zone/", ParcelFloodZoneView.as_view(), name="api_parcel_flood_zone"),
]