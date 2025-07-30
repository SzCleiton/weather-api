from unittest.mock import patch
from django.test import TestCase
from ..services.openweather_service import OpenWeatherService

class OpenWeatherServiceTest(TestCase):
    @patch('requests.get')
    def test_get_current_weather_success(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {"main": {"temp": 25}}
        mock_response.raise_for_status.return_value = None

        service = OpenWeatherService(api_key="fake_key")
        result = service.get_current_weather("Test City")

        self.assertEqual(result, {"main": {"temp": 25}})
        mock_get.assert_called_once()