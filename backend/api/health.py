import logging
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


@api_view(["GET"])
def health_check(request):
    """
    Health check endpoint for monitoring server status.
    
    GET /api/health/
    Returns: {"status": "healthy", "message": "Server is running"}
    """
    try:
        client_ip = request.META.get("REMOTE_ADDR")
        logger.debug(f"Health check from {client_ip}")
        return Response(
            {
                "status": "healthy",
                "message": "Server is running",
                "service": "HVAC AI API",
            },
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}", exc_info=True)
        return Response(
            {"status": "error", "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
