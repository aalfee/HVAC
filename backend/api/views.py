# /api/ root view
from django.http import JsonResponse

def api_root_view(request):
    return JsonResponse({
        "simulate": "/api/simulate/",
        "predict": "/api/predict/",
        "ingest": "/api/ingest/"
    })
from django.http import HttpResponse
# Root view for '/'
def root_view(request):
    return HttpResponse('<h2>🌬️ HVAC AI Platform API</h2><p>Welcome! Visit <a href="/api/">/api/</a> for API endpoints.</p>')
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from .serializers import SimulationInputSerializer, PredictionInputSerializer
from ml_models.predictor import predict
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from scripts.run_simulation import run as run_simulation

class SimulationView(APIView):
    def get(self, request):
        return Response({'message': 'Simulation endpoint'}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SimulationInputSerializer(data=request.data)
        if serializer.is_valid():
            # Here you would call the simulation logic, e.g., EnergyPlus wrapper
            # For now, just call the stub
            run_simulation()
            # Save result to DB if needed
            return Response({'result': 'Simulation run complete'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PredictionView(APIView):
    def get(self, request):
        return Response({'message': 'Prediction endpoint'}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PredictionInputSerializer(data=request.data)
        if serializer.is_valid():
            sensor_data = serializer.validated_data['sensor_data']
            # Ensure sensor_data is a list of lists (n_samples, 3)
            if not isinstance(sensor_data[0], list):
                sensor_data = [sensor_data]
            try:
                preds = predict(sensor_data)
                # Save prediction to DB if needed
                return Response({'prediction': preds}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Data ingestion endpoint (for time-series data)

class DataIngestionView(APIView):
    def get(self, request):
        # Return mock sensor data for demonstration
        data = [
            {"timestamp": "2025-10-03T10:00", "temp": 22.1, "humidity": 48, "co2": 420},
            {"timestamp": "2025-10-03T10:05", "temp": 22.3, "humidity": 47, "co2": 425},
            {"timestamp": "2025-10-03T10:10", "temp": 22.2, "humidity": 49, "co2": 430},
        ]
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        # Here you would process and store incoming time-series data
        # For now, just acknowledge receipt
        return Response({'message': 'Data ingested'}, status=status.HTTP_201_CREATED)
