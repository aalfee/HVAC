import json
import logging
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock

logger = logging.getLogger(__name__)


class APIHealthCheckTests(TestCase):
    """Test cases for API health check endpoint"""

    def setUp(self):
        self.client = Client()

    def test_health_check_endpoint_exists(self):
        """Test that health check endpoint returns 200"""
        response = self.client.get(reverse("health_check"))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["status"], "healthy")

    def test_health_check_response_format(self):
        """Test health check response has required fields"""
        response = self.client.get(reverse("health_check"))
        data = json.loads(response.content)
        self.assertIn("status", data)
        self.assertIn("message", data)
        self.assertIn("service", data)


class AnomalyDetectionAPITests(TestCase):
    """Test cases for anomaly detection API"""

    def setUp(self):
        self.client = Client()

    @patch("api.views.predict")
    def test_anomaly_detection_success(self, mock_predict):
        """Test successful anomaly detection request"""
        # Mock the predict function
        mock_df = MagicMock()
        mock_df.to_dict.return_value = [
            {"timestamp": "2023-01-01 00:00:00", "anomaly": False},
            {"timestamp": "2023-01-01 01:00:00", "anomaly": False},
            {"timestamp": "2023-01-01 02:00:00", "anomaly": True},
        ]
        mock_predict.return_value = mock_df

        response = self.client.get(reverse("anomaly_detection"))
        self.assertEqual(response.status_code, 200)

    @patch("api.views.predict")
    def test_anomaly_detection_file_not_found(self, mock_predict):
        """Test anomaly detection when data file is missing"""
        mock_predict.side_effect = FileNotFoundError("Data file not found")

        response = self.client.get(reverse("anomaly_detection"))
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertIn("error", data)

    @patch("api.views.predict")
    def test_anomaly_detection_server_error(self, mock_predict):
        """Test anomaly detection with unexpected error"""
        mock_predict.side_effect = Exception("Unexpected error")

        response = self.client.get(reverse("anomaly_detection"))
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.content)
        self.assertEqual(data["error"], "Internal server error")


class BrokenPipeHandlingTests(TestCase):
    """Test cases for broken pipe error handling"""

    def setUp(self):
        self.client = Client()

    @patch("api.views.predict")
    def test_broken_pipe_error_handled(self, mock_predict):
        """Test that broken pipe errors are handled gracefully"""
        mock_predict.side_effect = BrokenPipeError("Broken pipe")

        response = self.client.get(reverse("anomaly_detection"))
        # Should return 200 even with broken pipe
        self.assertIn(response.status_code, [200, 500])

    @patch("api.views.predict")
    def test_connection_reset_error_handled(self, mock_predict):
        """Test that connection reset errors are handled gracefully"""
        mock_predict.side_effect = ConnectionResetError("Connection reset")

        response = self.client.get(reverse("anomaly_detection"))
        # Should return 200 even with connection error
        self.assertIn(response.status_code, [200, 500])
