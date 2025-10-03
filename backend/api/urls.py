from django.urls import path
from .views import SimulationView, PredictionView, DataIngestionView, api_root_view

urlpatterns = [
    path('', api_root_view, name='api-root'),
    path('simulate/', SimulationView.as_view(), name='simulate'),
    path('predict/', PredictionView.as_view(), name='predict'),
    path('ingest/', DataIngestionView.as_view(), name='ingest'),
]
