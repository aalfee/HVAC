import logging


class IgnoreBrokenPipeFilter(logging.Filter):
    """
    Filter to suppress EPIPE (Broken pipe) errors from Django's logging output.
    These are expected when clients disconnect and don't need verbose logging.
    """

    def filter(self, record):
        """
        Return False to ignore the record (suppress it), True to keep it.
        """
        # Suppress broken pipe errors from Django's request logging
        if hasattr(record, 'exc_info') and record.exc_info:
            exc_type, exc_value, _ = record.exc_info
            if exc_type is BrokenPipeError:
                return False
            if exc_type is ConnectionResetError:
                return False

        # Also check the message itself
        message = record.getMessage()
        if "Broken pipe" in message and "BrokenPipeHandlerMiddleware" not in message:
            return False
        if "EPIPE" in message:
            return False

        return True
