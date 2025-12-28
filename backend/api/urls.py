from django.urls import path
from .views import anomaly_detection
from .health import health_check

urlpatterns = [
    path("health/", health_check, name="health_check"),
    path("anomalies/", anomaly_detection, name="anomaly_detection"),
]
