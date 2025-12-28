import logging
import socket
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF that handles broken pipe and connection errors gracefully.
    """
    # Handle broken pipe and connection errors
    if isinstance(exc, (BrokenPipeError, ConnectionResetError)):
        request = context.get('request')
        if request:
            client_ip = get_client_ip(request)
            logger.warning(
                f"Client disconnected ({type(exc).__name__}) from {client_ip} during "
                f"{request.method} {request.path}"
            )
        return Response({'detail': 'Connection closed'}, status=200)

    if isinstance(exc, socket.error):
        if "Broken pipe" in str(exc):
            request = context.get('request')
            if request:
                client_ip = get_client_ip(request)
                logger.warning(f"Socket error (broken pipe) from {client_ip}")
            return Response({'detail': 'Connection closed'}, status=200)

    # Use DRF's default exception handler for all other cases
    response = exception_handler(exc, context)

    if response is not None:
        # Log API errors
        request = context.get('request')
        if request:
            logger.warning(
                f"API Error: {response.status_code} - {request.method} {request.path} - "
                f"{response.data}"
            )

    return response


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
