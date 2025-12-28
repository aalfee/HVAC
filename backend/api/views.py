import logging
import socket
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ml_models.predictor import predict
from .serializers import AnomalySerializer

logger = logging.getLogger(__name__)


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


@api_view(["GET"])
def anomaly_detection(request):
    """
    Anomaly detection API endpoint.
    
    GET /api/anomalies/
    Returns a list of detected anomalies in HVAC data.
    """
    client_ip = get_client_ip(request)
    logger.debug(f"Anomaly detection request from {client_ip}")

    try:
        # Load and predict
        df = predict(csv_path="data/hvac_data.csv")
        data = df.to_dict(orient="records")
        logger.debug(f"Predictions generated: {len(data)} records for {client_ip}")

        # Validate data
        serializer = AnomalySerializer(data=data, many=True)
        if not serializer.is_valid():
            logger.warning(f"Serialization errors from {client_ip}: {serializer.errors}")
            return Response(
                {"error": "Invalid data format", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        logger.info(f"Anomaly detection successful for {client_ip}")
        return Response(serializer.data, status=status.HTTP_200_OK)

    except (BrokenPipeError, ConnectionResetError) as e:
        # Client disconnected - log but don't propagate error
        logger.warning(f"Client {client_ip} disconnected during anomaly detection: {type(e).__name__}")
        return Response(
            {"error": "Connection closed by client"},
            status=status.HTTP_200_OK,  # Return 200 even though client is gone
        )

    except FileNotFoundError as e:
        logger.error(f"Data file not found from {client_ip}: {str(e)}", exc_info=True)
        return Response(
            {"error": "Data file not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    except socket.error as e:
        if "Broken pipe" in str(e):
            logger.warning(f"Socket error (broken pipe) from {client_ip}")
            return Response(
                {"error": "Connection closed"},
                status=status.HTTP_200_OK,
            )
        logger.error(f"Socket error from {client_ip}: {str(e)}", exc_info=True)
        return Response(
            {"error": "Network error occurred"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    except Exception as e:
        logger.error(
            f"Unexpected error in anomaly detection from {client_ip}: {str(e)}",
            exc_info=True,
        )
        return Response(
            {"error": "Internal server error", "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
