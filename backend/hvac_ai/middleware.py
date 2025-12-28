import logging
import socket
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse

logger = logging.getLogger(__name__)


class BrokenPipeHandlerMiddleware(MiddlewareMixin):
    """
    Middleware to gracefully handle broken pipe errors from client disconnections.
    Prevents server crashes and logs the event for monitoring.
    """

    def process_request(self, request):
        """Log incoming requests"""
        logger.debug(f"Request: {request.method} {request.path} from {self.get_client_ip(request)}")
        return None

    def process_response(self, request, response):
        """Handle response and catch broken pipe errors"""
        try:
            # Log successful responses
            logger.debug(
                f"Response: {response.status_code} for {request.method} {request.path}"
            )
            return response
        except (BrokenPipeError, ConnectionResetError, socket.error) as e:
            # Log the broken pipe error but don't crash
            client_ip = self.get_client_ip(request)
            logger.warning(
                f"Broken pipe error from {client_ip} on {request.method} {request.path}: {str(e)}"
            )
            # Return an empty response to prevent further processing
            return HttpResponse(status=200)

    def process_exception(self, request, exception):
        """Handle exceptions, including broken pipe errors"""
        client_ip = self.get_client_ip(request)

        # Handle broken pipe and connection reset errors gracefully
        if isinstance(exception, (BrokenPipeError, ConnectionResetError)):
            logger.warning(
                f"Connection error from {client_ip} during {request.method} {request.path}: "
                f"{type(exception).__name__}"
            )
            return HttpResponse(status=200)

        if isinstance(exception, socket.error):
            if "Broken pipe" in str(exception):
                logger.warning(
                    f"Socket broken pipe from {client_ip} on {request.method} {request.path}"
                )
                return HttpResponse(status=200)

        # Log other exceptions normally
        logger.error(
            f"Exception for {request.method} {request.path}: {type(exception).__name__}: {str(exception)}",
            exc_info=True,
        )
        return None

    @staticmethod
    def get_client_ip(request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
