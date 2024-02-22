from django.urls import path
from . import views

urlpatterns = [
    path('location_topology/', views.LocationTopologyView.as_view(), name='location_topology'),
    path('topology/', views.TopologyView.as_view(), name='topology'),
]
