from django.urls import path
from .views import HomeView, ParcelGeoJSONView, ParcelNeighborsView

app_name = "geodata"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("api/parcels/", ParcelGeoJSONView.as_view(), name="api_parcels"),
    path("api/parcels/<int:pk>/neighbors/", ParcelNeighborsView.as_view(), name="api_parcel_neighbors"),
]