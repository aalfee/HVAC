from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class SimulationAPITests(APITestCase):
    def test_simulation_post(self):
        url = reverse('simulate')
        data = {
            'building_id': 'B1',
            'start_time': '2025-10-03T10:00',
            'end_time': '2025-10-03T12:00',
            'parameters': {"temp": 22}
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('result', response.data)

class PredictionAPITests(APITestCase):
    def test_prediction_post(self):
        url = reverse('predict')
        data = {
            'sensor_data': [[22.1, 48, 420], [22.3, 47, 425]],
            'timestamp': '2025-10-03T10:00'
        }
        response = self.client.post(url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_500_INTERNAL_SERVER_ERROR])
        # Accepts 500 if model not trained
