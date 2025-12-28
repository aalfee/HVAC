# HVAC API - Broken Pipe Error Handling & Improvements

## Overview
This document outlines the improvements made to handle broken pipe errors and improve overall API stability and logging.

## Changes Made

### 1. **Middleware: BrokenPipeHandlerMiddleware** (`hvac_ai/middleware.py`)
- **Purpose**: Catches and handles broken pipe errors from client disconnections
- **Features**:
  - Logs client IP and request details
  - Handles BrokenPipeError, ConnectionResetError, and socket.error gracefully
  - Prevents server crashes from abrupt client disconnections
  - Tracks client IP for monitoring

### 2. **Logging Filter: IgnoreBrokenPipeFilter** (`hvac_ai/logging_filters.py`)
- **Purpose**: Suppresses excessive broken pipe error logging
- **Features**:
  - Filters out expected BrokenPipeError exceptions
  - Filters out ConnectionResetError exceptions
  - Keeps critical errors visible

### 3. **Custom Exception Handler** (`hvac_ai/exceptions.py`)
- **Purpose**: Handles exceptions in REST Framework views
- **Features**:
  - Gracefully handles broken pipe and connection errors in API endpoints
  - Logs API errors with context
  - Returns appropriate HTTP status codes

### 4. **Enhanced Settings Configuration** (`hvac_ai/settings.py`)
Key additions:
```python
# Middleware
MIDDLEWARE += ['hvac_ai.middleware.BrokenPipeHandlerMiddleware']

# Logging with file rotation
LOGGING = {
    'handlers': {
        'console': {...},      # Stream to console with filtering
        'file': {...},         # Rotating file handler (10MB max)
        'error_file': {...},   # Separate error log
    }
}

# REST Framework Configuration
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'hvac_ai.exceptions.custom_exception_handler',
}

# Connection settings
CONN_MAX_AGE = 600  # 10 minute connection timeout
DATA_UPLOAD_MAX_MEMORY_SIZE = 2621440  # 2.5 MB
```

### 5. **Enhanced API Views** (`api/views.py`)
- **anomaly_detection()**: 
  - Comprehensive error handling for broken pipe, socket, and file errors
  - Client IP logging for monitoring
  - Proper HTTP status codes
  - Detailed error messages for debugging

### 6. **Health Check Endpoint** (`api/health.py`)
- **Purpose**: Simple endpoint to verify server health
- **Endpoint**: `GET /api/health/`
- **Response**: `{"status": "healthy", "message": "Server is running"}`

### 7. **Improved Test Suite** (`api/tests_improved.py`)
- Tests for health check endpoint
- Tests for anomaly detection success and failure scenarios
- Tests for broken pipe and connection reset error handling

## Logging

### Log Files
- **`logs/django.log`**: General application logs (rotating, 10MB max)
- **`logs/error.log`**: Error-level logs only (rotating, 10MB max)

### Log Format
```
[LEVEL] TIMESTAMP - logger_name - function:line - message
[INFO] 27/Dec/2025 22:46:38 - hvac_ai.middleware - process_response:41 - Response: 200 for GET /api/anomalies/
```

### Log Levels
- **Console**: DEBUG level (all messages)
- **File**: INFO level (info and above)
- **Error File**: ERROR level (errors only)

## Running Tests

```bash
# Run all tests
python manage.py test

# Run specific test module
python manage.py test api.tests_improved

# Run with verbose output
python manage.py test -v 2
```

## Monitoring Broken Pipe Errors

To monitor broken pipe occurrences:

```bash
# Check for broken pipe messages in logs
grep "Broken pipe" logs/django.log

# Count broken pipe occurrences
grep -c "Broken pipe" logs/django.log

# View recent broken pipe errors
tail -n 100 logs/django.log | grep "Broken pipe"
```

## Troubleshooting

### Issue: Still seeing "Broken pipe from" errors
**Solution**: These are now logged by the middleware but don't crash the server. The errors come from the WSGI server itself (Gunicorn/uWSGI) when clients disconnect. This is expected behavior.

### Issue: Log files growing too large
**Solution**: Rotating file handlers automatically manage log size:
- Individual log files capped at 10MB
- Up to 5 backup files retained
- Automatic cleanup of old logs

### Issue: Need more detailed logging
**Solution**: In `settings.py`, change logger level:
```python
'loggers': {
    'api': {
        'level': 'DEBUG',  # Increase verbosity
        ...
    }
}
```

## Performance Considerations

1. **Connection Pooling**: Set `CONN_MAX_AGE = 600` for persistent connections
2. **Memory Limits**: Upload limits set to 2.5MB to prevent memory exhaustion
3. **Async Processing**: For long-running predictions, consider using Celery
4. **Caching**: Consider caching prediction results for identical requests

## Security Recommendations

1. **Environment Variables**: Move SECRET_KEY to environment variable
2. **DEBUG Mode**: Set `DEBUG = False` in production
3. **ALLOWED_HOSTS**: Restrict to actual domain names in production
4. **CSRF Protection**: Keep CSRF middleware enabled
5. **Rate Limiting**: Consider adding rate limiting middleware for API endpoints

## Future Improvements

1. Add database connection pooling (django-db-gevent or similar)
2. Implement request timeout handling
3. Add metrics collection (Prometheus integration)
4. Implement graceful shutdown handlers
5. Add circuit breaker pattern for external dependencies
6. Implement request queuing for high load scenarios
